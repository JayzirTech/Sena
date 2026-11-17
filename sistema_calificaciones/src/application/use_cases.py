"""
Capa de Aplicación: Casos de Uso.
Orquesta el flujo de datos entre la capa de dominio y los repositorios.
Diseñado para soportar confirmación previa antes de persistir.
"""
from datetime import date
from typing import List, Optional, Tuple
from src.domain.models import (
    Estudiante,
    Calificacion,
    BoletinEstudiante,
    ResumenAsignaturaSalon,
    ConsolidadoSalon,
    ASIGNATURAS,
    PERIODOS_VALIDOS
)
from src.domain.services import (
    generar_siguiente_id_estudiante,
    generar_correo_institucional,
    construir_boletin_estudiante,
    calcular_metricas_asignatura,
    calcular_consolidado_salon
)
from src.application.interfaces import (
    EstudianteRepositoryInterface,
    CalificacionRepositoryInterface
)


class RegistrarEstudianteUseCase:
    def __init__(self, repo_estudiantes: EstudianteRepositoryInterface):
        self.repo = repo_estudiantes

    def preparar_registro(self, documento: str, nombre_completo: str) -> Tuple[bool, str, Optional[Estudiante]]:
        """Valida y genera el borrador del estudiante (ID y Correo autogenerados)."""
        doc_limpio = documento.strip()
        nombre_limpio = nombre_completo.strip()

        if not doc_limpio:
            return False, "El documento de identidad no puede estar vacío.", None
        if not nombre_limpio or len(nombre_limpio.split()) < 2:
            return False, "Ingrese al menos un nombre y un apellido completo.", None

        # Validar si ya existe el documento
        if self.repo.buscar_por_documento(doc_limpio) is not None:
            return False, f"Ya existe un aprendiz registrado con el documento {doc_limpio}.", None

        estudiantes_actuales = self.repo.obtener_todos()
        ids_existentes = [e.id_estudiante for e in estudiantes_actuales]
        correos_existentes = [e.correo for e in estudiantes_actuales]

        nuevo_id = generar_siguiente_id_estudiante(ids_existentes)
        nuevo_correo = generar_correo_institucional(nombre_limpio, correos_existentes)

        borrador = Estudiante(
            id_estudiante=nuevo_id,
            documento=doc_limpio,
            nombre_completo=nombre_limpio.title(),
            correo=nuevo_correo
        )
        return True, "Borrador generado exitosamente.", borrador

    def confirmar_registro(self, estudiante: Estudiante) -> bool:
        """Persiste definitivamente al estudiante tras la confirmación del usuario."""
        self.repo.guardar(estudiante)
        return True


class RegistrarCalificacionUseCase:
    def __init__(
        self,
        repo_estudiantes: EstudianteRepositoryInterface,
        repo_calificaciones: CalificacionRepositoryInterface
    ):
        self.repo_est = repo_estudiantes
        self.repo_cal = repo_calificaciones

    def preparar_registro(
        self,
        id_estudiante: str,
        id_materia: str,
        periodo: int,
        nota: float
    ) -> Tuple[bool, str, Optional[Calificacion]]:
        """Valida reglas de negocio y genera el borrador de la calificación."""
        estudiante = self.repo_est.buscar_por_id(id_estudiante)
        if not estudiante:
            return False, f"El aprendiz con ID '{id_estudiante}' no existe.", None

        if id_materia not in ASIGNATURAS:
            return False, f"La asignatura '{id_materia}' no es válida.", None

        if periodo not in PERIODOS_VALIDOS:
            return False, f"El periodo debe ser un valor entre 1 y 4.", None

        if not (0.0 <= nota <= 100.0):
            return False, "La calificación debe estar entre 0.0 y 100.0.", None

        nuevo_id = self.repo_cal.obtener_siguiente_id()
        fecha_actual = date.today().isoformat()

        calificacion = Calificacion(
            id_calificacion=nuevo_id,
            id_estudiante=id_estudiante,
            id_materia=id_materia,
            periodo=periodo,
            nota=round(nota, 2),
            fecha=fecha_actual
        )
        return True, "Calificación validada correctamente.", calificacion

    def confirmar_registro(self, calificacion: Calificacion) -> bool:
        """Persiste definitivamente la calificación tras la confirmación."""
        self.repo_cal.guardar(calificacion)
        return True


class ModificarCalificacionUseCase:
    def __init__(self, repo_calificaciones: CalificacionRepositoryInterface):
        self.repo_cal = repo_calificaciones

    def ejecutar(self, id_calificacion: int, nueva_nota: float, nuevo_periodo: int) -> Tuple[bool, str]:
        if nuevo_periodo not in PERIODOS_VALIDOS:
            return False, "El periodo debe ser un valor entre 1 y 4."
        if not (0.0 <= nueva_nota <= 100.0):
            return False, "La calificación debe estar entre 0.0 y 100.0."

        todas = self.repo_cal.obtener_todas()
        objetivo = next((c for c in todas if c.id_calificacion == id_calificacion), None)
        if not objetivo:
            return False, f"No existe una calificación con ID {id_calificacion}."

        objetivo.nota = round(nueva_nota, 2)
        objetivo.periodo = nuevo_periodo
        objetivo.fecha = date.today().isoformat()
        self.repo_cal.actualizar(objetivo)
        return True, "Calificación actualizada exitosamente."


class EliminarCalificacionUseCase:
    def __init__(self, repo_calificaciones: CalificacionRepositoryInterface):
        self.repo_cal = repo_calificaciones

    def ejecutar(self, id_calificacion: int) -> Tuple[bool, str]:
        ok = self.repo_cal.eliminar(id_calificacion)
        if ok:
            return True, f"Calificación #{id_calificacion} eliminada exitosamente."
        return False, f"No se encontró la calificación con ID #{id_calificacion}."


class BuscarEstudiantesUseCase:
    def __init__(self, repo_estudiantes: EstudianteRepositoryInterface):
        self.repo = repo_estudiantes

    def buscar(self, termino: str) -> List[Estudiante]:
        """
        Busca aprendices por coincidencia en:
        - Número o código directo (ej. '1' o 'EST-0001')
        - Documento de identidad
        - Subcadena en nombres y apellidos
        """
        termino_limpio = termino.strip().lower()
        if not termino_limpio:
            return []

        todos = self.repo.obtener_activos()
        coincidencias = []

        # 1. Búsqueda por ID directo numérico o exacto
        if termino_limpio.isdigit():
            formato_id = f"EST-{int(termino_limpio):04d}".lower()
            for e in todos:
                if e.id_estudiante.lower() == formato_id or e.documento == termino_limpio:
                    if e not in coincidencias:
                        coincidencias.append(e)

        # 2. Búsqueda por coincidencia de texto (ID con prefijo, nombre, documento largo o correo)
        for e in todos:
            if e in coincidencias:
                continue
            id_match = termino_limpio in e.id_estudiante.lower()
            nom_match = termino_limpio in e.nombre_completo.lower()
            correo_match = termino_limpio in e.correo.lower()
            doc_match = (termino_limpio in e.documento.lower()) if len(termino_limpio) >= 4 else (termino_limpio == e.documento)

            if id_match or nom_match or correo_match or doc_match:
                coincidencias.append(e)

        return coincidencias


class EliminarEstudianteUseCase:
    def __init__(self, repo_estudiantes: EstudianteRepositoryInterface):
        self.repo_est = repo_estudiantes

    def ejecutar(self, id_estudiante: str) -> Tuple[bool, str]:
        est = self.repo_est.buscar_por_id(id_estudiante, solo_activos=True)
        if not est:
            return False, f"El aprendiz con ID '{id_estudiante}' no existe o ya se encuentra inactivo."
        ok = self.repo_est.desactivar(id_estudiante)
        if ok:
            return True, f"El aprendiz [{est.id_estudiante}] {est.nombre_completo} ha sido eliminado del portal (borrado lógico aplicado)."
        return False, "Error al actualizar el estado del estudiante."


class GenerarBoletinEstudianteUseCase:
    def __init__(
        self,
        repo_estudiantes: EstudianteRepositoryInterface,
        repo_calificaciones: CalificacionRepositoryInterface
    ):
        self.repo_est = repo_estudiantes
        self.repo_cal = repo_calificaciones

    def ejecutar(self, id_estudiante: str) -> Optional[BoletinEstudiante]:
        estudiante = self.repo_est.buscar_por_id(id_estudiante, solo_activos=True)
        if not estudiante:
            return None

        todas_cal = self.repo_cal.obtener_todas()
        activos_est = self.repo_est.obtener_activos()

        # Calcular promedio general del salón para comparativa
        consolidado = calcular_consolidado_salon(activos_est, todas_cal)
        promedio_salon = consolidado.promedio_general_salon

        return construir_boletin_estudiante(estudiante, todas_cal, promedio_salon)


class GenerarReporteAsignaturaUseCase:
    def __init__(
        self,
        repo_estudiantes: EstudianteRepositoryInterface,
        repo_calificaciones: CalificacionRepositoryInterface
    ):
        self.repo_est = repo_estudiantes
        self.repo_cal = repo_calificaciones

    def ejecutar(self, id_materia: str, periodo_filtro: Optional[int] = None) -> ResumenAsignaturaSalon:
        calificaciones = self.repo_cal.obtener_todas()
        estudiantes = self.repo_est.obtener_activos()
        return calcular_metricas_asignatura(id_materia, calificaciones, estudiantes, periodo_filtro)


class GenerarConsolidadoSalonUseCase:
    def __init__(
        self,
        repo_estudiantes: EstudianteRepositoryInterface,
        repo_calificaciones: CalificacionRepositoryInterface
    ):
        self.repo_est = repo_estudiantes
        self.repo_cal = repo_calificaciones

    def ejecutar(self) -> ConsolidadoSalon:
        estudiantes = self.repo_est.obtener_activos()
        calificaciones = self.repo_cal.obtener_todas()
        return calcular_consolidado_salon(estudiantes, calificaciones)


class ObtenerMetricasEstadoSistemaUseCase:
    def __init__(
        self,
        repo_estudiantes: EstudianteRepositoryInterface,
        repo_calificaciones: CalificacionRepositoryInterface
    ):
        self.repo_est = repo_estudiantes
        self.repo_cal = repo_calificaciones

    def ejecutar(self) -> dict:
        total_activos = len(self.repo_est.obtener_activos())
        total_cal = len(self.repo_cal.obtener_todas())
        return {
            "total_estudiantes": total_activos,
            "total_calificaciones": total_cal,
            "archivos_activos": ["data/estudiantes.csv", "data/calificaciones.csv"]
        }
