"""
Capa de Dominio: Servicios y Lógica de Negocio Pura.
Incluye generador de correos anti-colisión, generador de IDs secuenciales
y motores de cálculo de promedios para los 4 periodos académicos.
"""
import unicodedata
import re
from typing import List, Dict, Set, Optional
from src.domain.models import (
    Estudiante,
    Calificacion,
    ASIGNATURAS,
    PERIODOS_VALIDOS,
    UMBRAL_APROBACION,
    ResumenPeriodoMateria,
    ResumenAsignaturaEstudiante,
    BoletinEstudiante,
    ResumenAsignaturaSalon,
    FilaConsolidadoSalon,
    ConsolidadoSalon
)


def normalizar_texto(texto: str) -> str:
    """Remueve tildes, diéresis, convierte a minúsculas y caracteres alfanuméricos."""
    texto = texto.strip().lower()
    # Descomponer caracteres con acento
    nfkd = unicodedata.normalize('NFKD', texto)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    sin_tildes = sin_tildes.replace('ñ', 'n')
    # Reemplazar espacios y caracteres no alfanuméricos por puntos
    limpio = re.sub(r'[^a-z0-9]+', '.', sin_tildes).strip('.')
    return limpio


def generar_correo_institucional(nombre_completo: str, correos_existentes: List[str]) -> str:
    """
    Genera correo formato 'nombre.apellido@sena.edu.co'.
    Garantiza unicidad añadiendo sufijos numéricos ante colisiones (ej. carlos.ramirez2@...).
    """
    partes = [p for p in normalizar_texto(nombre_completo).split('.') if p]
    if not partes:
        nombre_base = "aprendiz"
        apellido_base = "sena"
    elif len(partes) == 1:
        nombre_base = partes[0]
        apellido_base = "estudiante"
    elif len(partes) == 2:
        nombre_base = partes[0]
        apellido_base = partes[1]
    elif len(partes) == 3:
        # Ej: "Ana María Gómez" -> ana.gomez
        nombre_base = partes[0]
        apellido_base = partes[-1]
    else:
        # Ej: "Juan David Pérez Restrepo" -> juan.perez
        nombre_base = partes[0]
        apellido_base = partes[2]

    usuario_base = f"{nombre_base}.{apellido_base}"
    dominio = "@sena.edu.co"
    correos_set = {c.strip().lower() for c in correos_existentes}

    candidato = f"{usuario_base}{dominio}"
    if candidato not in correos_set:
        return candidato

    # Resolver colisión
    contador = 2
    while True:
        candidato = f"{usuario_base}{contador}{dominio}"
        if candidato not in correos_set:
            return candidato
        contador += 1


def generar_siguiente_id_estudiante(ids_existentes: List[str]) -> str:
    """Calcula el siguiente ID secuencial con formato EST-0001 a EST-9999."""
    max_num = 0
    for id_est in ids_existentes:
        id_limpio = id_est.strip().upper()
        if id_limpio.startswith("EST-"):
            parte_num = id_limpio.replace("EST-", "")
            if parte_num.isdigit():
                max_num = max(max_num, int(parte_num))
    nuevo_num = max_num + 1
    return f"EST-{nuevo_num:04d}"


def calcular_promedio(valores: List[float]) -> float:
    """Calcula media aritmética redondeada a 2 decimales."""
    if not valores:
        return 0.0
    return round(sum(valores) / len(valores), 2)


def evaluar_aprobacion(nota_o_promedio: float) -> bool:
    """Evalúa si una calificación cumple la condición de aprobación (>= 70.0)."""
    return round(nota_o_promedio, 2) >= UMBRAL_APROBACION


def construir_boletin_estudiante(
    estudiante: Estudiante,
    calificaciones: List[Calificacion],
    promedio_salon: float = 0.0
) -> BoletinEstudiante:
    """Construye el boletín académico detallado por periodos y acumulado anual."""
    notas_estudiante = [c for c in calificaciones if c.id_estudiante == estudiante.id_estudiante]

    resumenes_asignaturas: Dict[str, ResumenAsignaturaEstudiante] = {}
    definitivas_list: List[float] = []

    for codigo_materia, nombre_materia in ASIGNATURAS.items():
        periodos_dict: Dict[int, ResumenPeriodoMateria] = {}
        promedios_periodos_registrados: List[float] = []

        for p in PERIODOS_VALIDOS:
            notas_p = [c.nota for c in notas_estudiante if c.id_materia == codigo_materia and c.periodo == p]
            prom_p = calcular_promedio(notas_p) if notas_p else 0.0
            periodos_dict[p] = ResumenPeriodoMateria(
                periodo=p,
                notas=notas_p,
                promedio=prom_p,
                aprobado=evaluar_aprobacion(prom_p) if notas_p else False
            )
            if notas_p:
                promedios_periodos_registrados.append(prom_p)

        # Regla explícita: La definitiva anual se calcula dividiendo estrictamente entre 4 periodos,
        # independientemente de si hay notas registradas o no (los periodos vacíos computan como 0.0)
        suma_promedios_periodos = sum(periodos_dict[p].promedio for p in PERIODOS_VALIDOS)
        definitiva = round(suma_promedios_periodos / 4.0, 2)
        aprobada_mat = evaluar_aprobacion(definitiva)

        resumenes_asignaturas[codigo_materia] = ResumenAsignaturaEstudiante(
            id_materia=codigo_materia,
            nombre_materia=nombre_materia,
            periodos=periodos_dict,
            definitiva_anual=definitiva,
            aprobado=aprobada_mat
        )
        definitivas_list.append(definitiva)

    # Promedio General del Año (Promedio estricto de las 5 asignaturas)
    promedio_general = round(sum(definitivas_list) / 5.0, 2) if definitivas_list else 0.0
    aprobado_ano = evaluar_aprobacion(promedio_general)

    total_aprobadas = sum(1 for r in resumenes_asignaturas.values() if r.aprobado and r.definitiva_anual > 0)
    total_reprobadas = sum(1 for r in resumenes_asignaturas.values() if not r.aprobado and r.definitiva_anual > 0)

    # Mejor y peor materia
    materias_con_nota = [r for r in resumenes_asignaturas.values() if r.definitiva_anual > 0]
    mejor_mat = max(materias_con_nota, key=lambda r: r.definitiva_anual).nombre_materia if materias_con_nota else None
    peor_mat = min(materias_con_nota, key=lambda r: r.definitiva_anual).nombre_materia if materias_con_nota else None

    diferencia = round(promedio_general - promedio_salon, 2) if promedio_salon > 0 else 0.0

    return BoletinEstudiante(
        estudiante=estudiante,
        asignaturas=resumenes_asignaturas,
        promedio_general_anual=promedio_general,
        aprobado_ano=aprobado_ano,
        total_aprobadas=total_aprobadas,
        total_reprobadas=total_reprobadas,
        mejor_materia=mejor_mat,
        peor_materia=peor_mat,
        diferencia_vs_salon=diferencia
    )


def calcular_metricas_asignatura(
    id_materia: str,
    calificaciones: List[Calificacion],
    estudiantes: List[Estudiante],
    periodo_filtro: Optional[int] = None
) -> ResumenAsignaturaSalon:
    """Calcula las métricas de rendimiento grupal para una asignatura específica."""
    notas_materia = [c for c in calificaciones if c.id_materia == id_materia]
    if periodo_filtro is not None:
        notas_materia = [c for c in notas_materia if c.periodo == periodo_filtro]

    nombre_mat = ASIGNATURAS.get(id_materia, id_materia)
    valores_notas = [c.nota for c in notas_materia]

    if not valores_notas:
        return ResumenAsignaturaSalon(
            id_materia=id_materia,
            nombre_materia=nombre_mat,
            total_evaluaciones=0,
            promedio_grupal=0.0,
            total_aprobados=0,
            total_reprobados=0,
            tasa_aprobacion=0.0,
            nota_maxima=0.0,
            nota_minima=0.0
        )

    # Agrupar por estudiante para contar aprobados
    notas_por_est: Dict[str, List[float]] = {}
    for c in notas_materia:
        notas_por_est.setdefault(c.id_estudiante, []).append(c.nota)

    aprobados = 0
    reprobados = 0
    for n_list in notas_por_est.values():
        prom_est = calcular_promedio(n_list)
        if evaluar_aprobacion(prom_est):
            aprobados += 1
        else:
            reprobados += 1

    total_est_evaluados = len(notas_por_est)
    tasa = round((aprobados / total_est_evaluados * 100), 1) if total_est_evaluados > 0 else 0.0

    return ResumenAsignaturaSalon(
        id_materia=id_materia,
        nombre_materia=nombre_mat,
        total_evaluaciones=len(valores_notas),
        promedio_grupal=calcular_promedio(valores_notas),
        total_aprobados=aprobados,
        total_reprobados=reprobados,
        tasa_aprobacion=tasa,
        nota_maxima=max(valores_notas),
        nota_minima=min(valores_notas)
    )


def calcular_consolidado_salon(
    estudiantes: List[Estudiante],
    calificaciones: List[Calificacion]
) -> ConsolidadoSalon:
    """Construye la sábana de notas del salón completo y sus métricas globales."""
    filas: List[FilaConsolidadoSalon] = []
    promedios_generales: List[float] = []

    for est in estudiantes:
        boletin = construir_boletin_estudiante(est, calificaciones)
        promedios_por_materia = {
            cod: boletin.asignaturas[cod].definitiva_anual
            for cod in ASIGNATURAS.keys()
        }
        filas.append(FilaConsolidadoSalon(
            id_estudiante=est.id_estudiante,
            nombre_completo=est.nombre_completo,
            promedios_materias=promedios_por_materia,
            promedio_final=boletin.promedio_general_anual,
            aprobado=boletin.aprobado_ano
        ))
        if boletin.promedio_general_anual > 0:
            promedios_generales.append(boletin.promedio_general_anual)

    total_est = len(estudiantes)
    aprobados = sum(1 for f in filas if f.aprobado and f.promedio_final > 0)
    reprobados = sum(1 for f in filas if not f.aprobado and f.promedio_final > 0)
    tasa = round((aprobados / total_est * 100), 1) if total_est > 0 else 0.0

    promedio_salon = calcular_promedio(promedios_generales) if promedios_generales else 0.0

    filas_con_nota = [f for f in filas if f.promedio_final > 0]
    mejor_fila = max(filas_con_nota, key=lambda f: f.promedio_final) if filas_con_nota else None

    return ConsolidadoSalon(
        filas=filas,
        promedio_general_salon=promedio_salon,
        total_estudiantes=total_est,
        total_aprobados=aprobados,
        total_reprobados=reprobados,
        tasa_aprobacion=tasa,
        estudiante_destacado=mejor_fila.nombre_completo if mejor_fila else None,
        mejor_promedio=mejor_fila.promedio_final if mejor_fila else 0.0
    )
