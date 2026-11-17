"""
Script para Inyectar Datos de Prueba (Seeder).
Comando de ejecución:
    python seed.py
o también:
    python main.py --seed
"""
import sys
import os
from datetime import date

# Asegurar path raíz
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.infrastructure.repositories import (
    CsvEstudianteRepository,
    CsvCalificacionRepository
)
from src.domain.models import Estudiante, Calificacion


def inyectar_datos_prueba():
    print("=" * 80)
    print("        INYECCIÓN DE DATOS DE PRUEBA - SISTEMA DE CALIFICACIONES SENA")
    print("=" * 80)

    repo_est = CsvEstudianteRepository("data/estudiantes.csv")
    repo_cal = CsvCalificacionRepository("data/calificaciones.csv")

    estudiantes_demo = [
        ("1001234567", "Ana Maria Gomez Restrepo"),
        ("1009876543", "Carlos Mario Ramirez Lopez"),
        ("1011121314", "Laura Marcela Restrepo Perez"),
        ("1022334455", "Juan David Morales Castro"),
        ("1033445566", "Sofia Valentina Herrera Mejia")
    ]

    print("\n[1/2] Inyectando aprendices de prueba...")
    estudiantes_registrados = []
    for doc, nombre in estudiantes_demo:
        existente = repo_est.buscar_por_documento(doc)
        if not existente:
            # Calcular ID y correo
            todos = repo_est.obtener_todos()
            nuevo_num = len(todos) + 1
            nuevo_id = f"EST-{nuevo_num:04d}"
            partes = nombre.lower().split()
            correo = f"{partes[0]}.{partes[2]}@sena.edu.co" if len(partes) >= 3 else f"{partes[0]}.{partes[1]}@sena.edu.co"
            nuevo_est = Estudiante(
                id_estudiante=nuevo_id,
                documento=doc,
                nombre_completo=nombre.title(),
                correo=correo,
                estado="ACTIVO"
            )
            repo_est.guardar(nuevo_est)
            estudiantes_registrados.append(nuevo_est)
            print(f"  -> Creado: [{nuevo_id}] {nuevo_est.nombre_completo} ({correo})")
        else:
            estudiantes_registrados.append(existente)
            print(f"  -> Ya existe: [{existente.id_estudiante}] {existente.nombre_completo}")

    print("\n[2/2] Inyectando calificaciones de prueba...")
    calificaciones_actuales = repo_cal.obtener_todas()
    if not calificaciones_actuales:
        fecha_hoy = date.today().isoformat()
        notas_demo = [
            # Ana Gómez (EST-0001): Promedio destacado en programación y matemáticas
            ("EST-0001", "MAT", 1, 85.0),
            ("EST-0001", "MAT", 2, 90.0),
            ("EST-0001", "MAT", 3, 88.0),
            ("EST-0001", "MAT", 4, 92.0),
            ("EST-0001", "PROG", 1, 95.0),
            ("EST-0001", "PROG", 2, 100.0),
            ("EST-0001", "PROG", 3, 98.0),
            ("EST-0001", "PROG", 4, 96.0),
            ("EST-0001", "LIT", 1, 80.0),
            ("EST-0001", "LIT", 2, 85.0),
            ("EST-0001", "SOC", 1, 78.0),
            ("EST-0001", "QUI", 1, 72.0),

            # Carlos Ramírez (EST-0002): Rendimiento mixto con periodos por nivelar
            ("EST-0002", "MAT", 1, 60.0),
            ("EST-0002", "MAT", 2, 65.0),
            ("EST-0002", "QUI", 1, 55.0),
            ("EST-0002", "QUI", 2, 62.0),
            ("EST-0002", "PROG", 1, 75.0),
            ("EST-0002", "PROG", 2, 80.0),
            ("EST-0002", "LIT", 1, 70.0),
            ("EST-0002", "SOC", 1, 68.0),

            # Laura Restrepo (EST-0003): Cuadro de honor
            ("EST-0003", "MAT", 1, 95.0),
            ("EST-0003", "MAT", 2, 92.0),
            ("EST-0003", "PROG", 1, 100.0),
            ("EST-0003", "PROG", 2, 98.0),
            ("EST-0003", "LIT", 1, 90.0),
            ("EST-0003", "SOC", 1, 92.0),
            ("EST-0003", "QUI", 1, 88.0),

            # Juan Morales (EST-0004): Buen desempeño
            ("EST-0004", "MAT", 1, 75.0),
            ("EST-0004", "PROG", 1, 82.0),
            ("EST-0004", "LIT", 1, 85.0),
            ("EST-0004", "SOC", 1, 80.0),
            ("EST-0004", "QUI", 1, 76.0),

            # Sofia Herrera (EST-0005): En riesgo académico
            ("EST-0005", "MAT", 1, 50.0),
            ("EST-0005", "PROG", 1, 65.0),
            ("EST-0005", "QUI", 1, 58.0),
            ("EST-0005", "LIT", 1, 62.0),
            ("EST-0005", "SOC", 1, 60.0),
        ]

        for id_est, cod_mat, per, val in notas_demo:
            nuevo_id = repo_cal.obtener_siguiente_id()
            c = Calificacion(
                id_calificacion=nuevo_id,
                id_estudiante=id_est,
                id_materia=cod_mat,
                periodo=per,
                nota=val,
                fecha=fecha_hoy
            )
            repo_cal.guardar(c)
        print(f"  -> {len(notas_demo)} calificaciones inyectadas exitosamente.")
    else:
        print(f"  -> Ya existen {len(calificaciones_actuales)} calificaciones en base de datos. No se duplicaron.")

    print("\n" + "=" * 80)
    print(" >> ¡Datos de prueba inyectados correctamente!")
    print(" >> Puede ejecutar 'python main.py' para navegar el portal.")
    print("=" * 80)


if __name__ == "__main__":
    inyectar_datos_prueba()
