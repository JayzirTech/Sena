"""
Punto de Entrada Principal del Portal de Calificaciones SENA.
Configura e inyecta las dependencias según los principios de Clean Architecture.
"""
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.infrastructure.repositories import (
    CsvEstudianteRepository,
    CsvCalificacionRepository
)
from src.application.use_cases import (
    RegistrarEstudianteUseCase,
    EliminarEstudianteUseCase,
    RegistrarCalificacionUseCase,
    ModificarCalificacionUseCase,
    EliminarCalificacionUseCase,
    BuscarEstudiantesUseCase,
    GenerarBoletinEstudianteUseCase,
    GenerarReporteAsignaturaUseCase,
    GenerarConsolidadoSalonUseCase,
    ObtenerMetricasEstadoSistemaUseCase
)
from src.presentation.controller import ConsoleController


def main():
    # 1. Capa de Infraestructura (Persistencia CSV en data/)
    repo_estudiantes = CsvEstudianteRepository("data/estudiantes.csv")
    repo_calificaciones = CsvCalificacionRepository("data/calificaciones.csv")

    # 2. Capa de Aplicación (Casos de Uso)
    uc_reg_estudiante = RegistrarEstudianteUseCase(repo_estudiantes)
    uc_elim_estudiante = EliminarEstudianteUseCase(repo_estudiantes)
    uc_reg_calificacion = RegistrarCalificacionUseCase(repo_estudiantes, repo_calificaciones)
    uc_mod_calificacion = ModificarCalificacionUseCase(repo_calificaciones)
    uc_elim_calificacion = EliminarCalificacionUseCase(repo_calificaciones)
    uc_buscar_estudiantes = BuscarEstudiantesUseCase(repo_estudiantes)
    uc_boletin = GenerarBoletinEstudianteUseCase(repo_estudiantes, repo_calificaciones)
    uc_rep_asignatura = GenerarReporteAsignaturaUseCase(repo_estudiantes, repo_calificaciones)
    uc_consolidado = GenerarConsolidadoSalonUseCase(repo_estudiantes, repo_calificaciones)
    uc_metricas = ObtenerMetricasEstadoSistemaUseCase(repo_estudiantes, repo_calificaciones)

    # 3. Capa de Presentación (Controlador de Consola)
    controlador = ConsoleController(
        uc_reg_estudiante=uc_reg_estudiante,
        uc_elim_estudiante=uc_elim_estudiante,
        uc_reg_calificacion=uc_reg_calificacion,
        uc_mod_calificacion=uc_mod_calificacion,
        uc_elim_calificacion=uc_elim_calificacion,
        uc_buscar_estudiantes=uc_buscar_estudiantes,
        uc_boletin=uc_boletin,
        uc_rep_asignatura=uc_rep_asignatura,
        uc_consolidado=uc_consolidado,
        uc_metricas=uc_metricas
    )

    # 4. Iniciar la aplicación interactiva
    controlador.ejecutar()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--seed", "-s", "seed"):
        from seed import inyectar_datos_prueba
        inyectar_datos_prueba()
        sys.exit(0)

    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n>> Sesión finalizada por el usuario. ¡Hasta luego!")
