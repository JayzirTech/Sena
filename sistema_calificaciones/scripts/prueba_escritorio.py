"""
Script de Prueba de Escritorio Automatizada (Desk Check).
Simula la carga de datos de prueba y genera las salidas requeridas por el reto SENA.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.infrastructure.repositories import (
    CsvEstudianteRepository,
    CsvCalificacionRepository
)
from src.application.use_cases import (
    RegistrarEstudianteUseCase,
    RegistrarCalificacionUseCase,
    GenerarBoletinEstudianteUseCase,
    GenerarReporteAsignaturaUseCase,
    GenerarConsolidadoSalonUseCase
)
from src.domain.models import ASIGNATURAS


def ejecutar_prueba():
    print("=" * 80)
    print(" INICIANDO PRUEBA DE ESCRITORIO - SISTEMA DE CALIFICACIONES SENA")
    print("=" * 80)

    repo_est = CsvEstudianteRepository("data/estudiantes.csv")
    repo_cal = CsvCalificacionRepository("data/calificaciones.csv")

    uc_reg_est = RegistrarEstudianteUseCase(repo_est)
    uc_reg_cal = RegistrarCalificacionUseCase(repo_est, repo_cal)
    uc_boletin = GenerarBoletinEstudianteUseCase(repo_est, repo_cal)
    uc_rep_mat = GenerarReporteAsignaturaUseCase(repo_est, repo_cal)
    uc_cons = GenerarConsolidadoSalonUseCase(repo_est, repo_cal)

    # 1. Registrar Estudiantes si no existen
    estudiantes_prueba = [
        ("1001234567", "Ana Maria Gomez"),
        ("1009876543", "Carlos Mario Ramirez"),
        ("1011121314", "Laura Marcela Restrepo")
    ]

    print("\n[Paso 1] Verificando y registrando aprendices de prueba...")
    for doc, nom in estudiantes_prueba:
        existente = repo_est.buscar_por_documento(doc)
        if not existente:
            ok, msg, borrador = uc_reg_est.preparar_registro(doc, nom)
            if ok and borrador:
                uc_reg_est.confirmar_registro(borrador)
                print(f" -> Registrado: [{borrador.id_estudiante}] {borrador.nombre_completo} ({borrador.correo})")
        else:
            print(f" -> Ya existía: [{existente.id_estudiante}] {existente.nombre_completo}")

    # 2. Registrar Calificaciones de prueba
    calificaciones_prueba = [
        # Ana Gómez (EST-0001): Promedio alto (~85)
        ("EST-0001", "MAT", 1, 80.0),
        ("EST-0001", "MAT", 2, 85.0),
        ("EST-0001", "PROG", 1, 95.0),
        ("EST-0001", "PROG", 2, 90.0),
        ("EST-0001", "LIT", 1, 88.0),
        ("EST-0001", "SOC", 1, 82.0),
        ("EST-0001", "QUI", 1, 75.0),

        # Carlos Ramírez (EST-0002): Caso en riesgo (< 70 en química y mat)
        ("EST-0002", "MAT", 1, 60.0),
        ("EST-0002", "MAT", 2, 65.0),
        ("EST-0002", "QUI", 1, 55.0),
        ("EST-0002", "PROG", 1, 75.0),
        ("EST-0002", "LIT", 1, 70.0),
        ("EST-0002", "SOC", 1, 68.0),

        # Laura Restrepo (EST-0003): Cuadro de honor (> 90)
        ("EST-0003", "MAT", 1, 95.0),
        ("EST-0003", "PROG", 1, 100.0),
        ("EST-0003", "LIT", 1, 92.0),
        ("EST-0003", "SOC", 1, 88.0),
        ("EST-0003", "QUI", 1, 90.0),
    ]

    print("\n[Paso 2] Asentando calificaciones de prueba...")
    notas_existentes = repo_cal.obtener_todas()
    if not notas_existentes:
        for id_est, mat, per, nota in calificaciones_prueba:
            ok, msg, borrador = uc_reg_cal.preparar_registro(id_est, mat, per, nota)
            if ok and borrador:
                uc_reg_cal.confirmar_registro(borrador)
        print(f" -> {len(calificaciones_prueba)} calificaciones asentadas exitosamente.")
    else:
        print(f" -> Ya existían {len(notas_existentes)} calificaciones registradas.")

    # 3. Comprobación de Resultados
    print("\n[Paso 3] Métricas del Consolidado del Salón:")
    cons = uc_cons.ejecutar()
    print(f" • Total Estudiantes:        {cons.total_estudiantes}")
    print(f" • Promedio General Salón:   {cons.promedio_general_salon:.2f}")
    print(f" • Aprobados:                {cons.total_aprobados} ({cons.tasa_aprobacion:.1f}%)")
    print(f" • Reprobados:               {cons.total_reprobados}")
    print(f" • Mejor Aprendiz:           {cons.estudiante_destacado} ({cons.mejor_promedio:.2f})")

    print("\n[Paso 4] Verificación de Boletín Individual (EST-0001):")
    bol = uc_boletin.ejecutar("EST-0001")
    if bol:
        print(f" • Aprendiz:                 {bol.estudiante.nombre_completo}")
        print(f" • Promedio Anual:           {bol.promedio_general_anual:.2f}")
        print(f" • Estado:                   {'APROBADO' if bol.aprobado_ano else 'REPROBADO'}")
        print(f" • Mejor Asignatura:         {bol.mejor_materia}")

    print("\n" + "=" * 80)
    print(" PRUEBA DE ESCRITORIO COMPLETADA CON ÉXITO [OK]")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_prueba()
