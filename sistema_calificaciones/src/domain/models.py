"""
Capa de Dominio: Entidades y Modelos de Datos.
No tiene dependencias de persistencia (CSV) ni de interfaz de usuario.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Catálogo fijo de las 5 asignaturas oficiales
ASIGNATURAS = {
    "MAT": "Matemáticas",
    "LIT": "Literatura",
    "SOC": "Ciencias Sociales",
    "QUI": "Química",
    "PROG": "Programación de Software"
}

PERIODOS_VALIDOS = (1, 2, 3, 4)
UMBRAL_APROBACION = 70.0


@dataclass
class Estudiante:
    id_estudiante: str          # EST-0001
    documento: str              # Documento real (CC/TI)
    nombre_completo: str
    correo: str                 # Autogenerado institucional
    estado: str = "ACTIVO"      # ACTIVO o INACTIVO (Soft Delete)


@dataclass
class Calificacion:
    id_calificacion: int
    id_estudiante: str
    id_materia: str             # Código: MAT, LIT, etc.
    periodo: int                # 1, 2, 3 o 4
    nota: float                 # 0.0 a 100.0
    fecha: str                  # YYYY-MM-DD


@dataclass
class ResumenPeriodoMateria:
    periodo: int
    notas: List[float]
    promedio: float
    aprobado: bool


@dataclass
class ResumenAsignaturaEstudiante:
    id_materia: str
    nombre_materia: str
    periodos: Dict[int, ResumenPeriodoMateria]
    definitiva_anual: float
    aprobado: bool


@dataclass
class BoletinEstudiante:
    estudiante: Estudiante
    asignaturas: Dict[str, ResumenAsignaturaEstudiante]
    promedio_general_anual: float
    aprobado_ano: bool
    total_aprobadas: int
    total_reprobadas: int
    mejor_materia: Optional[str] = None
    peor_materia: Optional[str] = None
    diferencia_vs_salon: float = 0.0


@dataclass
class ResumenAsignaturaSalon:
    id_materia: str
    nombre_materia: str
    total_evaluaciones: int
    promedio_grupal: float
    total_aprobados: int
    total_reprobados: int
    tasa_aprobacion: float
    nota_maxima: float
    nota_minima: float


@dataclass
class FilaConsolidadoSalon:
    id_estudiante: str
    nombre_completo: str
    promedios_materias: Dict[str, float]  # MAT: 85.0, PROG: 90.0
    promedio_final: float
    aprobado: bool


@dataclass
class ConsolidadoSalon:
    filas: List[FilaConsolidadoSalon]
    promedio_general_salon: float
    total_estudiantes: int
    total_aprobados: int
    total_reprobados: int
    tasa_aprobacion: float
    estudiante_destacado: Optional[str] = None
    mejor_promedio: float = 0.0
