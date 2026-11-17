"""
Capa de Presentación: Controlador de Flujo de Navegación.
Gestiona el Menú Principal, Submenús, Selección Inteligente y
aplica confirmación obligatoria previa a toda modificación de datos.
"""
from typing import Optional, List
from src.domain.models import ASIGNATURAS, PERIODOS_VALIDOS, Estudiante
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
from src.presentation.console import (
    limpiar_pantalla,
    pausar,
    pedir_confirmacion,
    mostrar_banner_principal,
    mostrar_ficha_estudiante_registrado,
    mostrar_boletin_estudiante,
    mostrar_reporte_asignatura,
    mostrar_comparativo_asignaturas,
    mostrar_consolidado_salon
)


class ConsoleController:
    def __init__(
        self,
        uc_reg_estudiante: RegistrarEstudianteUseCase,
        uc_elim_estudiante: EliminarEstudianteUseCase,
        uc_reg_calificacion: RegistrarCalificacionUseCase,
        uc_mod_calificacion: ModificarCalificacionUseCase,
        uc_elim_calificacion: EliminarCalificacionUseCase,
        uc_buscar_estudiantes: BuscarEstudiantesUseCase,
        uc_boletin: GenerarBoletinEstudianteUseCase,
        uc_rep_asignatura: GenerarReporteAsignaturaUseCase,
        uc_consolidado: GenerarConsolidadoSalonUseCase,
        uc_metricas: ObtenerMetricasEstadoSistemaUseCase
    ):
        self.uc_reg_estudiante = uc_reg_estudiante
        self.uc_elim_estudiante = uc_elim_estudiante
        self.uc_reg_calificacion = uc_reg_calificacion
        self.uc_mod_calificacion = uc_mod_calificacion
        self.uc_elim_calificacion = uc_elim_calificacion
        self.uc_buscar_estudiantes = uc_buscar_estudiantes
        self.uc_boletin = uc_boletin
        self.uc_rep_asignatura = uc_rep_asignatura
        self.uc_consolidado = uc_consolidado
        self.uc_metricas = uc_metricas

    def ejecutar(self) -> None:
        """Bucle principal de la aplicación."""
        while True:
            metricas = self.uc_metricas.ejecutar()
            mostrar_banner_principal(metricas)

            print("\n  --- MÓDULO DE GESTIÓN DE APRENDICES ---")
            print("  [1] Registrar nuevo estudiante (Sin límites)")
            print("  [2] Eliminar estudiante (Borrado Lógico / No se borran notas en BD)")
            print("\n  --- MÓDULO DE CALIFICACIONES ---")
            print("  [3] Registrar calificación (Por periodo 1-4 y asignatura)")
            print("  [4] Modificar o Eliminar calificación existente")
            print("\n  --- MÓDULO DE ANALÍTICA Y REPORTES ---")
            print("  [5] Reportes: ENFOQUE ESTUDIANTES  --->")
            print("  [6] Reportes: ENFOQUE ASIGNATURAS Y SALÓN  --->")
            print("\n  --- SISTEMA ---")
            print("  [0] Salir del sistema")
            print("=" * 88)

            opcion = input(" Ingrese una opción [0-6]: ").strip()

            if opcion == "1":
                self._accion_registrar_estudiante()
            elif opcion == "2":
                self._accion_eliminar_estudiante()
            elif opcion == "3":
                self._accion_registrar_calificacion()
            elif opcion == "4":
                self._accion_gestionar_calificaciones_existentes()
            elif opcion == "5":
                self._submenu_estudiantes()
            elif opcion == "6":
                self._submenu_asignaturas_salon()
            elif opcion == "0":
                if pedir_confirmacion("¿Está seguro de que desea salir del portal?"):
                    limpiar_pantalla()
                    print("\n>> Gracias por utilizar el Portal de Gestión Académica SENA. ¡Hasta pronto!\n")
                    break
            else:
                print(" [!] Opción no válida. Intente de nuevo.")
                pausar()

    # -------------------------------------------------------------
    # SUBMENÚS
    # -------------------------------------------------------------
    def _submenu_estudiantes(self) -> None:
        while True:
            limpiar_pantalla()
            print("=" * 88)
            print("                     MÓDULO DE REPORTES: ENFOQUE ESTUDIANTE")
            print("=" * 88)
            print("  [1] Boletín Consolidado Final de Año (4 Periodos + Definitiva + Estado)")
            print("  [2] Buscar historial y notas de un aprendiz")
            print("  [0] << Volver al Menú Principal")
            print("=" * 88)

            op = input(" Ingrese una opción [0-2]: ").strip()
            if op == "0":
                break
            elif op in ("1", "2"):
                estudiante = self._seleccionar_estudiante()
                if estudiante:
                    boletin = self.uc_boletin.ejecutar(estudiante.id_estudiante)
                    if boletin:
                        mostrar_boletin_estudiante(boletin)
                        pausar()
            else:
                print(" [!] Opción no válida.")
                pausar()

    def _submenu_asignaturas_salon(self) -> None:
        while True:
            limpiar_pantalla()
            print("=" * 88)
            print("               MÓDULO DE REPORTES: ENFOQUE ASIGNATURAS Y SALÓN")
            print("=" * 88)
            print("  [1] Rendimiento Detallado de una Asignatura (Periodo o Anual)")
            print("  [2] Resumen Comparativo de las 5 Asignaturas (Vista Macro)")
            print("  [3] Sábana General Consolidada del Salón (Promedio Grupal y Aprobación)")
            print("  [0] << Volver al Menú Principal")
            print("=" * 88)

            op = input(" Ingrese una opción [0-3]: ").strip()
            if op == "0":
                break
            elif op == "1":
                self._accion_reporte_materia()
            elif op == "2":
                self._accion_comparativo_asignaturas()
            elif op == "3":
                self._accion_consolidado_salon()
            else:
                print(" [!] Opción no válida.")
                pausar()

    # -------------------------------------------------------------
    # ACCIONES TRANSACCIONALES CON CONFIRMACIÓN
    # -------------------------------------------------------------
    def _accion_registrar_estudiante(self) -> None:
        limpiar_pantalla()
        print("=" * 88)
        print("                              REGISTRO DE NUEVO APRENDIZ")
        print("=" * 88)
        print(" [INFO] El ID y el Correo Institucional serán autogenerados automáticamente.\n")

        doc = input(" Ingrese Documento de Identidad (TI/CC): ").strip()
        nombre = input(" Ingrese Nombre completo del aprendiz: ").strip()

        ok, msg, borrador = self.uc_reg_estudiante.preparar_registro(doc, nombre)
        if not ok or borrador is None:
            print(f"\n [ERROR] {msg}")
            pausar()
            return

        # Vista previa para confirmación
        print("\n" + "-" * 60)
        print(" RESUMEN DEL NUEVO APRENDIZ A REGISTRAR:")
        print(f"  • Código asignado:      {borrador.id_estudiante}")
        print(f"  • Documento:            {borrador.documento}")
        print(f"  • Nombre completo:      {borrador.nombre_completo}")
        print(f"  • Correo generado:      {borrador.correo}")
        print("-" * 60)

        # Confirmación obligatoria previa
        if pedir_confirmacion("¿Desea confirmar y guardar este aprendiz en la base de datos?"):
            self.uc_reg_estudiante.confirmar_registro(borrador)
            mostrar_ficha_estudiante_registrado(borrador)
            pausar()
        else:
            print("\n [!] Operación cancelada por el usuario. No se guardaron cambios.")
            pausar()

    def _accion_eliminar_estudiante(self) -> None:
        limpiar_pantalla()
        print("=" * 88)
        print("                 ELIMINACIÓN DE APRENDIZ (BORRADO LÓGICO)")
        print("=" * 88)
        print(" [AVISO] Al eliminar un aprendiz, sus notas y registro permanecen en la base de datos")
        print("         para efectos de auditoría histórica, pero ya NO aparecerá en el portal.\n")

        estudiante = self._seleccionar_estudiante()
        if not estudiante:
            return

        print("\n" + "-" * 60)
        print(" RESUMEN DEL APRENDIZ A DAR DE BAJA:")
        print(f"  • Código:    {estudiante.id_estudiante}")
        print(f"  • Documento: {estudiante.documento}")
        print(f"  • Nombre:    {estudiante.nombre_completo}")
        print(f"  • Correo:    {estudiante.correo}")
        print("-" * 60)

        if pedir_confirmacion(f"¿Está COMPLETAMENTE SEGURO de eliminar al aprendiz {estudiante.nombre_completo}?"):
            ok, msg = self.uc_elim_estudiante.ejecutar(estudiante.id_estudiante)
            if ok:
                print(f"\n >> {msg}")
            else:
                print(f"\n [ERROR] {msg}")
            pausar()
        else:
            print("\n [!] Eliminación cancelada. El aprendiz sigue activo en el sistema.")
            pausar()

    def _accion_registrar_calificacion(self) -> None:
        limpiar_pantalla()
        print("=" * 88)
        print("                           REGISTRO DE CALIFICACIONES")
        print("=" * 88)

        estudiante = self._seleccionar_estudiante()
        if not estudiante:
            return

        # Seleccionar Asignatura
        print("\nSeleccione la Asignatura:")
        lista_materias = list(ASIGNATURAS.items())
        for idx, (cod, nom) in enumerate(lista_materias, 1):
            print(f"  [{idx}] {nom} [{cod}]")
        print("  [0] << Cancelar")

        try:
            op_mat = int(input("\nOpción de materia [0-5]: ").strip())
            if op_mat == 0:
                return
            if not (1 <= op_mat <= 5):
                print(" [!] Asignatura inválida.")
                pausar()
                return
            cod_materia, nom_materia = lista_materias[op_mat - 1]
        except ValueError:
            print(" [!] Debe ingresar un número.")
            pausar()
            return

        # Seleccionar Periodo
        try:
            periodo = int(input("Ingrese Periodo Académico (1, 2, 3 o 4): ").strip())
            if periodo not in PERIODOS_VALIDOS:
                print(" [!] Periodo inválido.")
                pausar()
                return
        except ValueError:
            print(" [!] Debe ingresar un número entero del 1 al 4.")
            pausar()
            return

        # Ingresar Nota
        try:
            nota = float(input("Ingrese Calificación (0.0 a 100.0): ").strip().replace(",", "."))
            if not (0.0 <= nota <= 100.0):
                print(" [!] La nota debe estar entre 0.0 y 100.0.")
                pausar()
                return
        except ValueError:
            print(" [!] Debe ingresar un valor numérico para la nota.")
            pausar()
            return

        ok, msg, borrador_cal = self.uc_reg_calificacion.preparar_registro(
            id_estudiante=estudiante.id_estudiante,
            id_materia=cod_materia,
            periodo=periodo,
            nota=nota
        )

        if not ok or borrador_cal is None:
            print(f"\n [ERROR] {msg}")
            pausar()
            return

        # Vista previa de la calificación
        print("\n" + "-" * 60)
        print(" RESUMEN DE LA CALIFICACIÓN A ASENTAR:")
        print(f"  • Aprendiz:     [{estudiante.id_estudiante}] {estudiante.nombre_completo}")
        print(f"  • Asignatura:   {nom_materia} [{cod_materia}]")
        print(f"  • Periodo:      {periodo}")
        print(f"  • Calificación: {nota:.1f}")
        print("-" * 60)

        # Confirmación obligatoria previa
        if pedir_confirmacion("¿Confirmar el guardado de esta calificación en el archivo CSV?"):
            self.uc_reg_calificacion.confirmar_registro(borrador_cal)
            print("\n >> ¡Calificación asentada y guardada con éxito en 'data/calificaciones.csv'!")
            pausar()
        else:
            print("\n [!] Operación cancelada. La calificación no fue guardada.")
            pausar()

    def _accion_gestionar_calificaciones_existentes(self) -> None:
        limpiar_pantalla()
        print("=" * 88)
        print("               MODIFICACIÓN Y ELIMINACIÓN DE CALIFICACIONES")
        print("=" * 88)

        estudiante = self._seleccionar_estudiante()
        if not estudiante:
            return

        todas_cal = self.uc_reg_calificacion.repo_cal.obtener_por_estudiante(estudiante.id_estudiante)
        if not todas_cal:
            print(f"\n [!] El aprendiz {estudiante.nombre_completo} no tiene calificaciones registradas.")
            pausar()
            return

        print(f"\nCalificaciones registradas para {estudiante.nombre_completo}:")
        print("-" * 88)
        for idx, c in enumerate(todas_cal, 1):
            nom_mat = ASIGNATURAS.get(c.id_materia, c.id_materia)
            print(f"  [{idx}] ID: #{c.id_calificacion} | {nom_mat:<24} | Periodo: {c.periodo} | Nota: {c.nota:<5.1f} | Fecha: {c.fecha}")
        print("-" * 88)

        try:
            op_cal = int(input(f"\nSeleccione el número de la calificación [1-{len(todas_cal)}]: ").strip())
            if not (1 <= op_cal <= len(todas_cal)):
                print(" [!] Selección fuera de rango.")
                pausar()
                return
            cal_sel = todas_cal[op_cal - 1]
        except ValueError:
            print(" [!] Debe ingresar un número.")
            pausar()
            return

        print("\n¿Qué acción desea realizar con esta calificación?")
        print("  [1] Modificar nota o periodo")
        print("  [2] Eliminar calificación definitivamente")
        print("  [0] Cancelar")
        accion = input("Seleccione [0-2]: ").strip()

        if accion == "1":
            try:
                nuevo_periodo = int(input(f"Nuevo periodo (Actual: {cal_sel.periodo}) [1-4]: ").strip())
                nueva_nota = float(input(f"Nueva nota (Actual: {cal_sel.nota}) [0.0 - 100.0]: ").strip().replace(",", "."))
            except ValueError:
                print(" [!] Datos numéricos inválidos.")
                pausar()
                return

            print("\n" + "-" * 60)
            print(" RESUMEN DEL CAMBIO PENDIENTE:")
            print(f"  • Calificación ID: #{cal_sel.id_calificacion}")
            print(f"  • Periodo:        {cal_sel.periodo} -> {nuevo_periodo}")
            print(f"  • Nota:           {cal_sel.nota:.1f} -> {nueva_nota:.1f}")
            print("-" * 60)

            if pedir_confirmacion("¿Confirmar y aplicar esta modificación en el archivo CSV?"):
                ok, msg = self.uc_mod_calificacion.ejecutar(cal_sel.id_calificacion, nueva_nota, nuevo_periodo)
                if ok:
                    print(f"\n >> {msg}")
                else:
                    print(f"\n [ERROR] {msg}")
                pausar()
            else:
                print("\n [!] Modificación cancelada por el usuario.")
                pausar()

        elif accion == "2":
            print("\n" + "-" * 60)
            print(f" [PELIGRO] Se eliminará la calificación #{cal_sel.id_calificacion} (Nota: {cal_sel.nota})")
            print("-" * 60)
            if pedir_confirmacion("¿Está COMPLETAMENTE SEGURO de eliminar esta calificación del archivo CSV?"):
                ok, msg = self.uc_elim_calificacion.ejecutar(cal_sel.id_calificacion)
                if ok:
                    print(f"\n >> {msg}")
                else:
                    print(f"\n [ERROR] {msg}")
                pausar()
            else:
                print("\n [!] Eliminación cancelada por el usuario.")
                pausar()

    # -------------------------------------------------------------
    # REPORTES
    # -------------------------------------------------------------
    def _accion_reporte_materia(self) -> None:
        limpiar_pantalla()
        print("=" * 88)
        print("                   CONSULTA DE REPORTE POR ASIGNATURA")
        print("=" * 88)
        lista_materias = list(ASIGNATURAS.items())
        for idx, (cod, nom) in enumerate(lista_materias, 1):
            print(f"  [{idx}] {nom} [{cod}]")
        print("  [0] << Cancelar")

        try:
            op = int(input("\nSeleccione asignatura [0-5]: ").strip())
            if op == 0:
                return
            if not (1 <= op <= 5):
                print(" [!] Opción inválida.")
                pausar()
                return
            cod_mat, nom_mat = lista_materias[op - 1]
        except ValueError:
            print(" [!] Ingrese un número válido.")
            pausar()
            return

        filtro = input("Filtrar por periodo específico (1-4) o [ENTER] para acumulado anual: ").strip()
        periodo_filtro = int(filtro) if filtro in ("1", "2", "3", "4") else None

        rep = self.uc_rep_asignatura.ejecutar(cod_mat, periodo_filtro)
        mostrar_reporte_asignatura(rep, periodo_filtro)
        pausar()

    def _accion_comparativo_asignaturas(self) -> None:
        reportes = [self.uc_rep_asignatura.ejecutar(cod) for cod in ASIGNATURAS.keys()]
        mostrar_comparativo_asignaturas(reportes)
        pausar()

    def _accion_consolidado_salon(self) -> None:
        cons = self.uc_consolidado.ejecutar()
        mostrar_consolidado_salon(cons)
        pausar()

    # -------------------------------------------------------------
    # SELECTOR INTELIGENTE ESCALABLE (1.000+ ESTUDIANTES)
    # -------------------------------------------------------------
    def _seleccionar_estudiante(self) -> Optional[Estudiante]:
        """Motor de búsqueda y selección indexado para 1 a 1000+ aprendices activos."""
        todos = self.uc_reg_estudiante.repo.obtener_activos()
        if not todos:
            print("\n [!] No hay aprendices registrados actualmente. Registre uno primero en la opción [1].")
            pausar()
            return None

        # Si son 7 o menos, los listamos directamente para comodidad
        if len(todos) <= 7:
            print("\nSeleccione el aprendiz:")
            for idx, e in enumerate(todos, 1):
                print(f"  [{idx}] {e.id_estudiante} - {e.nombre_completo} (Doc: {e.documento})")
            print("  [0] << Cancelar")
            try:
                op = int(input(f"\nSeleccione opción [0-{len(todos)}]: ").strip())
                if op == 0:
                    return None
                if 1 <= op <= len(todos):
                    return todos[op - 1]
            except ValueError:
                pass
            print(" [!] Selección no válida.")
            pausar()
            return None

        # Si son más de 7 (hasta 1.000+), activamos el buscador inteligente
        print("\n" + "-" * 70)
        termino = input(" Buscar aprendiz por ID (ej. 4 o EST-0004), Documento o Nombre [0 para salir]: ").strip()
        if termino == "0":
            return None
        coincidencias = self.uc_buscar_estudiantes.buscar(termino)

        if not coincidencias:
            print(f" [!] No se encontraron aprendices con el criterio '{termino}'.")
            pausar()
            return None

        if len(coincidencias) == 1:
            print(f" >> Coincidencia exacta: [{coincidencias[0].id_estudiante}] {coincidencias[0].nombre_completo}")
            return coincidencias[0]

        print(f"\n Coincidencias encontradas ({len(coincidencias)}):")
        for idx, e in enumerate(coincidencias[:15], 1):  # Limitar vista a 15 por pantalla
            print(f"  [{idx}] {e.id_estudiante} - {e.nombre_completo} (Doc: {e.documento})")
        print("  [0] << Cancelar")

        try:
            op = int(input(f"\nSeleccione opción [0-{min(len(coincidencias), 15)}]: ").strip())
            if op == 0:
                return None
            if 1 <= op <= len(coincidencias):
                return coincidencias[op - 1]
        except ValueError:
            pass

        print(" [!] Selección cancelada o no válida.")
        pausar()
        return None
