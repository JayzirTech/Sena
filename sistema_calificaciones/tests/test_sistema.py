"""
Pruebas Unitarias de Verificación (Clean Architecture & Data Integrity).
Valida fórmulas matemáticas, generación de IDs, correos anti-colisión y persistencia.
"""
import unittest
import os
import shutil
from src.domain.services import (
    generar_siguiente_id_estudiante,
    generar_correo_institucional,
    calcular_promedio,
    evaluar_aprobacion,
    construir_boletin_estudiante,
    calcular_consolidado_salon
)
from src.domain.models import Estudiante, Calificacion
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
    BuscarEstudiantesUseCase
)


class TestDominioYServicios(unittest.TestCase):

    def test_generador_id_secuencial(self):
        self.assertEqual(generar_siguiente_id_estudiante([]), "EST-0001")
        self.assertEqual(
            generar_siguiente_id_estudiante(["EST-0001", "EST-0002"]),
            "EST-0003"
        )
        self.assertEqual(
            generar_siguiente_id_estudiante(["EST-0009", "EST-0999"]),
            "EST-1000"
        )

    def test_generador_correo_y_anti_colision(self):
        # Caso estándar con tildes
        correo1 = generar_correo_institucional("Ána María Gómez", [])
        self.assertEqual(correo1, "ana.gomez@sena.edu.co")

        # Caso con colisión (mismo nombre y apellido)
        correo2 = generar_correo_institucional("Ana Gómez", ["ana.gomez@sena.edu.co"])
        self.assertEqual(correo2, "ana.gomez2@sena.edu.co")

        correo3 = generar_correo_institucional("Ana Gómez", ["ana.gomez@sena.edu.co", "ana.gomez2@sena.edu.co"])
        self.assertEqual(correo3, "ana.gomez3@sena.edu.co")

    def test_regla_aprobacion(self):
        self.assertTrue(evaluar_aprobacion(70.0))
        self.assertTrue(evaluar_aprobacion(85.5))
        self.assertFalse(evaluar_aprobacion(69.99))
        self.assertFalse(evaluar_aprobacion(50.0))

    def test_calculo_boletin_4_periodos(self):
        est = Estudiante("EST-0001", "12345", "Carlos Pérez", "carlos.perez@sena.edu.co")
        calificaciones = [
            # Matemáticas: P1 (80, 90 -> 85), P2 (75 -> 75), P3 (0), P4 (0)
            # Definitiva estricta entre 4: (85 + 75 + 0 + 0) / 4 = 40.0
            Calificacion(1, "EST-0001", "MAT", 1, 80.0, "2026-03-01"),
            Calificacion(2, "EST-0001", "MAT", 1, 90.0, "2026-03-15"),
            Calificacion(3, "EST-0001", "MAT", 2, 75.0, "2026-06-01"),
        ]
        boletin = construir_boletin_estudiante(est, calificaciones)
        res_mat = boletin.asignaturas["MAT"]

        self.assertEqual(res_mat.periodos[1].promedio, 85.0)
        self.assertEqual(res_mat.periodos[2].promedio, 75.0)
        self.assertEqual(res_mat.definitiva_anual, 40.0)
        self.assertFalse(res_mat.aprobado)

        # Si completa los 4 periodos con notas aprobatorias
        calificaciones.extend([
            Calificacion(4, "EST-0001", "MAT", 3, 80.0, "2026-09-01"),
            Calificacion(5, "EST-0001", "MAT", 4, 80.0, "2026-11-01")
        ])
        # Ahora: (85 + 75 + 80 + 80) / 4 = 320 / 4 = 80.0
        boletin_completo = construir_boletin_estudiante(est, calificaciones)
        self.assertEqual(boletin_completo.asignaturas["MAT"].definitiva_anual, 80.0)
        self.assertTrue(boletin_completo.asignaturas["MAT"].aprobado)


class TestCasosDeUsoYPersistencia(unittest.TestCase):
    CARPETA_TEST = "data_test"

    def setUp(self):
        if os.path.exists(self.CARPETA_TEST):
            shutil.rmtree(self.CARPETA_TEST)
        os.makedirs(self.CARPETA_TEST, exist_ok=True)
        self.repo_est = CsvEstudianteRepository(os.path.join(self.CARPETA_TEST, "estudiantes.csv"))
        self.repo_cal = CsvCalificacionRepository(os.path.join(self.CARPETA_TEST, "calificaciones.csv"))

    def tearDown(self):
        if os.path.exists(self.CARPETA_TEST):
            shutil.rmtree(self.CARPETA_TEST)

    def test_flujo_confirmacion_estudiante(self):
        uc = RegistrarEstudianteUseCase(self.repo_est)
        ok, msg, borrador = uc.preparar_registro("1002345678", "Laura Restrepo")
        self.assertTrue(ok)
        self.assertEqual(borrador.id_estudiante, "EST-0001")
        self.assertEqual(borrador.correo, "laura.restrepo@sena.edu.co")

        # Antes de confirmar, no debe haber nada en el repo
        self.assertEqual(len(self.repo_est.obtener_todos()), 0)

        # Confirmamos
        uc.confirmar_registro(borrador)
        guardados = self.repo_est.obtener_todos()
        self.assertEqual(len(guardados), 1)
        self.assertEqual(guardados[0].nombre_completo, "Laura Restrepo")

    def test_buscador_estudiantes(self):
        self.repo_est.guardar(Estudiante("EST-0001", "1001", "Ana Gomez", "ana.gomez@sena.edu.co"))
        self.repo_est.guardar(Estudiante("EST-0002", "1002", "Carlos Ramirez", "carlos.ramirez@sena.edu.co"))

        uc_buscar = BuscarEstudiantesUseCase(self.repo_est)

        # Búsqueda por número
        res1 = uc_buscar.buscar("1")
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0].id_estudiante, "EST-0001")

        # Búsqueda por nombre
        res2 = uc_buscar.buscar("ramirez")
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0].id_estudiante, "EST-0002")


    def test_modificar_y_eliminar_calificacion(self):
        cal = Calificacion(1, "EST-0001", "MAT", 1, 60.0, "2026-03-01")
        self.repo_cal.guardar(cal)
        self.assertEqual(len(self.repo_cal.obtener_todas()), 1)

        # Modificar
        uc_mod = ModificarCalificacionUseCase(self.repo_cal)
        ok, msg = uc_mod.ejecutar(id_calificacion=1, nueva_nota=95.0, nuevo_periodo=2)
        self.assertTrue(ok)
        cal_mod = self.repo_cal.obtener_todas()[0]
        self.assertEqual(cal_mod.nota, 95.0)
        self.assertEqual(cal_mod.periodo, 2)

        # Eliminar
        uc_elim = EliminarCalificacionUseCase(self.repo_cal)
        ok_elim, msg_elim = uc_elim.ejecutar(id_calificacion=1)
        self.assertTrue(ok_elim)
        self.assertEqual(len(self.repo_cal.obtener_todas()), 0)


    def test_borrado_logico_estudiante(self):
        est = Estudiante("EST-0001", "1001", "Ana Gomez", "ana.gomez@sena.edu.co", "ACTIVO")
        self.repo_est.guardar(est)
        self.assertEqual(len(self.repo_est.obtener_activos()), 1)

        uc_elim_est = EliminarEstudianteUseCase(self.repo_est)
        ok, msg = uc_elim_est.ejecutar("EST-0001")
        self.assertTrue(ok)

        # En la base de datos CSV sigue existiendo la fila física (auditoría)
        self.assertEqual(len(self.repo_est.obtener_todos()), 1)
        self.assertEqual(self.repo_est.obtener_todos()[0].estado, "INACTIVO")

        # Para el portal (activos) ya no existe
        self.assertEqual(len(self.repo_est.obtener_activos()), 0)
        self.assertIsNone(self.repo_est.buscar_por_id("EST-0001", solo_activos=True))


if __name__ == "__main__":
    unittest.main()
