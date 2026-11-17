"""
Capa de Infraestructura: Repositorios basados en archivos planos CSV.
Maneja la lectura y persistencia atómica en disco en la carpeta data/.
"""
import csv
import os
from typing import List, Optional
from src.domain.models import Estudiante, Calificacion
from src.application.interfaces import (
    EstudianteRepositoryInterface,
    CalificacionRepositoryInterface
)


class CsvEstudianteRepository(EstudianteRepositoryInterface):
    def __init__(self, ruta_archivo: str = "data/estudiantes.csv"):
        self.ruta_archivo = ruta_archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        if not os.path.exists(self.ruta_archivo) or os.path.getsize(self.ruta_archivo) == 0:
            with open(self.ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(["id_estudiante", "documento", "nombre_completo", "correo", "estado"])

    def obtener_todos(self) -> List[Estudiante]:
        self._asegurar_archivo()
        estudiantes: List[Estudiante] = []
        with open(self.ruta_archivo, mode="r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila and fila.get("id_estudiante"):
                    estado_val = fila.get("estado", "ACTIVO").strip().upper() if fila.get("estado") else "ACTIVO"
                    estudiantes.append(Estudiante(
                        id_estudiante=fila["id_estudiante"].strip(),
                        documento=fila["documento"].strip(),
                        nombre_completo=fila["nombre_completo"].strip(),
                        correo=fila["correo"].strip(),
                        estado=estado_val
                    ))
        return estudiantes

    def obtener_activos(self) -> List[Estudiante]:
        return [e for e in self.obtener_todos() if e.estado == "ACTIVO"]

    def buscar_por_id(self, id_estudiante: str, solo_activos: bool = True) -> Optional[Estudiante]:
        id_buscado = id_estudiante.strip().upper()
        pool = self.obtener_activos() if solo_activos else self.obtener_todos()
        for e in pool:
            if e.id_estudiante.upper() == id_buscado:
                return e
        return None

    def buscar_por_documento(self, documento: str, solo_activos: bool = False) -> Optional[Estudiante]:
        doc_buscado = documento.strip()
        pool = self.obtener_activos() if solo_activos else self.obtener_todos()
        for e in pool:
            if e.documento == doc_buscado:
                return e
        return None

    def guardar(self, estudiante: Estudiante) -> None:
        self._asegurar_archivo()
        with open(self.ruta_archivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow([
                estudiante.id_estudiante,
                estudiante.documento,
                estudiante.nombre_completo,
                estudiante.correo,
                estudiante.estado
            ])

    def desactivar(self, id_estudiante: str) -> bool:
        """Borrado lógico: actualiza estado a INACTIVO sin borrar datos."""
        todos = self.obtener_todos()
        encontrado = False
        for e in todos:
            if e.id_estudiante.upper() == id_estudiante.strip().upper():
                e.estado = "INACTIVO"
                encontrado = True
                break

        if not encontrado:
            return False

        with open(self.ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["id_estudiante", "documento", "nombre_completo", "correo", "estado"])
            for e in todos:
                escritor.writerow([e.id_estudiante, e.documento, e.nombre_completo, e.correo, e.estado])
        return True


class CsvCalificacionRepository(CalificacionRepositoryInterface):
    def __init__(self, ruta_archivo: str = "data/calificaciones.csv"):
        self.ruta_archivo = ruta_archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        if not os.path.exists(self.ruta_archivo) or os.path.getsize(self.ruta_archivo) == 0:
            with open(self.ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(["id_calificacion", "id_estudiante", "id_materia", "periodo", "nota", "fecha"])

    def obtener_todas(self) -> List[Calificacion]:
        self._asegurar_archivo()
        calificaciones: List[Calificacion] = []
        with open(self.ruta_archivo, mode="r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila and fila.get("id_calificacion"):
                    calificaciones.append(Calificacion(
                        id_calificacion=int(fila["id_calificacion"]),
                        id_estudiante=fila["id_estudiante"].strip(),
                        id_materia=fila["id_materia"].strip().upper(),
                        periodo=int(fila["periodo"]),
                        nota=float(fila["nota"]),
                        fecha=fila["fecha"].strip()
                    ))
        return calificaciones

    def obtener_por_estudiante(self, id_estudiante: str) -> List[Calificacion]:
        id_buscado = id_estudiante.strip().upper()
        return [c for c in self.obtener_todas() if c.id_estudiante.upper() == id_buscado]

    def obtener_por_materia(self, id_materia: str) -> List[Calificacion]:
        mat_buscada = id_materia.strip().upper()
        return [c for c in self.obtener_todas() if c.id_materia.upper() == mat_buscada]

    def obtener_siguiente_id(self) -> int:
        todas = self.obtener_todas()
        if not todas:
            return 1
        return max(c.id_calificacion for c in todas) + 1

    def guardar(self, calificacion: Calificacion) -> None:
        self._asegurar_archivo()
        with open(self.ruta_archivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow([
                calificacion.id_calificacion,
                calificacion.id_estudiante,
                calificacion.id_materia,
                calificacion.periodo,
                calificacion.nota,
                calificacion.fecha
            ])

    def actualizar(self, calificacion: Calificacion) -> bool:
        todas = self.obtener_todas()
        encontrado = False
        nuevas = []
        for c in todas:
            if c.id_calificacion == calificacion.id_calificacion:
                nuevas.append(calificacion)
                encontrado = True
            else:
                nuevas.append(c)

        if not encontrado:
            return False

        with open(self.ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["id_calificacion", "id_estudiante", "id_materia", "periodo", "nota", "fecha"])
            for c in nuevas:
                escritor.writerow([c.id_calificacion, c.id_estudiante, c.id_materia, c.periodo, c.nota, c.fecha])
        return True

    def eliminar(self, id_calificacion: int) -> bool:
        todas = self.obtener_todas()
        nuevas = [c for c in todas if c.id_calificacion != id_calificacion]
        if len(nuevas) == len(todas):
            return False

        with open(self.ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["id_calificacion", "id_estudiante", "id_materia", "periodo", "nota", "fecha"])
            for c in nuevas:
                escritor.writerow([c.id_calificacion, c.id_estudiante, c.id_materia, c.periodo, c.nota, c.fecha])
        return True
