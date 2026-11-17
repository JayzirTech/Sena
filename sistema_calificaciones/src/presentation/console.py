"""
Capa de Presentación: Vistas de Consola y Formato Visual.
Manejo de limpieza de pantalla (cls/clear), banners, tablas formateadas,
fichas de confirmación y lectura segura con confirmación explícita (S/N).
"""
import os
from typing import List, Optional
from src.domain.models import (
    Estudiante,
    Calificacion,
    BoletinEstudiante,
    ResumenAsignaturaSalon,
    ConsolidadoSalon,
    ASIGNATURAS,
    PERIODOS_VALIDOS
)


def limpiar_pantalla() -> None:
    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensaje: str = "Presione [ENTER] para continuar...") -> None:
    """Pausa la ejecución para permitir lectura al usuario."""
    try:
        input(f"\n{mensaje}")
    except (KeyboardInterrupt, EOFError):
        pass


def pedir_confirmacion(pregunta: str) -> bool:
    """
    Solicita confirmación obligatoria al usuario (S/N).
    Retorna True si confirma, False en caso contrario.
    """
    while True:
        try:
            resp = input(f"\n>> {pregunta} (S/N): ").strip().upper()
            if resp in ("S", "SI", "Y", "YES"):
                return True
            if resp in ("N", "NO"):
                return False
            print(" [!] Respuesta inválida. Por favor escriba 'S' para confirmar o 'N' para cancelar.")
        except (KeyboardInterrupt, EOFError):
            return False


def mostrar_banner_principal(metricas: dict) -> None:
    limpiar_pantalla()
    print("=" * 88)
    print("             SISTEMA DE GESTIÓN ACADÉMICA Y CALIFICACIONES - SENA")
    print("                               (SALÓN ÚNICO)")
    print("=" * 88)
    print(" ESTADO DEL SISTEMA:")
    print(f"  • Estudiantes registrados: {metricas.get('total_estudiantes', 0)}")
    print(f"  • Calificaciones en base de datos: {metricas.get('total_calificaciones', 0)}")
    print("  • Persistencia: data/estudiantes.csv  |  data/calificaciones.csv  [ONLINE]")
    print("=" * 88)


def mostrar_ficha_estudiante_registrado(estudiante: Estudiante) -> None:
    """Ficha resumen con los datos definitivos asignados tras el registro."""
    limpiar_pantalla()
    print("=" * 88)
    print("                       ¡APRENDIZ REGISTRADO EXITOSAMENTE!")
    print("=" * 88)
    print(" Se ha guardado el nuevo registro en 'data/estudiantes.csv' con los siguientes datos:\n")
    print(f"  • Código de Aprendiz:    {estudiante.id_estudiante}")
    print(f"  • Documento (TI/CC):     {estudiante.documento}")
    print(f"  • Nombre Completo:       {estudiante.nombre_completo}")
    print(f"  • Correo Institucional:  {estudiante.correo}")
    print("  • Estado en Sistema:     ACTIVO (0 calificaciones asentadas)")
    print("=" * 88)


def mostrar_boletin_estudiante(boletin: BoletinEstudiante) -> None:
    limpiar_pantalla()
    e = boletin.estudiante
    print("=" * 88)
    print("                 BOLETÍN ACADÉMICO INDIVIDUAL - SALÓN 1 (SENA)")
    print("=" * 88)
    print("DATOS DEL APRENDIZ:")
    print(f" • Código / ID:      {e.id_estudiante}")
    print(f" • Nombre Completo:  {e.nombre_completo}")
    print(f" • Documento:        {e.documento}")
    print(f" • Correo:           {e.correo}")
    print("=" * 88)
    print(f"{'ASIGNATURA':<25} {'P1':<7} {'P2':<7} {'P3':<7} {'P4':<7} | {'DEFINITIVA':<10} | {'ESTADO':<12}")
    print("-" * 88)

    for cod, res in boletin.asignaturas.items():
        p1 = f"{res.periodos[1].promedio:.1f}" if res.periodos[1].notas else "-"
        p2 = f"{res.periodos[2].promedio:.1f}" if res.periodos[2].notas else "-"
        p3 = f"{res.periodos[3].promedio:.1f}" if res.periodos[3].notas else "-"
        p4 = f"{res.periodos[4].promedio:.1f}" if res.periodos[4].notas else "-"
        def_txt = f"{res.definitiva_anual:.2f}" if res.definitiva_anual > 0 else "-"
        estado = "APROBADA" if res.aprobado else ("NO APROBADA" if res.definitiva_anual > 0 else "SIN NOTAS")
        print(f"{res.nombre_materia:<25} {p1:<7} {p2:<7} {p3:<7} {p4:<7} | {def_txt:<10} | {estado:<12}")

    print("-" * 88)
    estado_final = "APROBADO" if boletin.aprobado_ano else "NO APROBADO"
    print("BALANCE ACADÉMICO DEL APRENDIZ:")
    print(f" • Promedio Ponderado General del Año: {boletin.promedio_general_anual:.2f}")
    print(f" • Estado Final del Curso:             {estado_final} (Corte >= 70.0)")
    print(f" • Asignaturas Aprobadas:              {boletin.total_aprobadas} / 5")
    if boletin.mejor_materia:
        print(f" • Asignatura con Mejor Rendimiento:   {boletin.mejor_materia}")
    if boletin.peor_materia and boletin.peor_materia != boletin.mejor_materia:
        print(f" • Asignatura a Reforzar:              {boletin.peor_materia}")

    signo = "+" if boletin.diferencia_vs_salon >= 0 else ""
    print("\nCOMPARATIVA CON EL SALÓN:")
    print(f" • Desempeño relativo: {signo}{boletin.diferencia_vs_salon:.2f} pts frente a la media del grupo.")
    print("=" * 88)


def mostrar_reporte_asignatura(rep: ResumenAsignaturaSalon, periodo_filtro: Optional[int] = None) -> None:
    limpiar_pantalla()
    filtro_txt = f" (PERIODO {periodo_filtro})" if periodo_filtro else " (ACUMULADO ANUAL)"
    print("=" * 88)
    print(f"            REPORTE DE ASIGNATURA: {rep.nombre_materia.upper()} [{rep.id_materia}]{filtro_txt}")
    print("=" * 88)
    print(f" • Total de evaluaciones registradas:  {rep.total_evaluaciones}")
    print(f" • Promedio grupal de la materia:      {rep.promedio_grupal:.2f}")
    print(f" • Calificación más alta:              {rep.nota_maxima:.1f}")
    print(f" • Calificación más baja:              {rep.nota_minima:.1f}")
    print(f" • Aprendices Aprobados:               {rep.total_aprobados} ({rep.tasa_aprobacion:.1f}%)")
    print(f" • Aprendices No Aprobados:            {rep.total_reprobados}")
    print("=" * 88)


def mostrar_comparativo_asignaturas(reportes: List[ResumenAsignaturaSalon]) -> None:
    limpiar_pantalla()
    print("=" * 88)
    print("                      RESUMEN COMPARATIVO DE ASIGNATURAS")
    print("=" * 88)
    print(f"{'CÓDIGO':<8} {'ASIGNATURA':<25} {'NOTAS':<8} {'PROM. GRUPO':<13} {'% APROBACIÓN':<15} {'ESTADO GRUPO':<15}")
    print("-" * 88)
    for r in reportes:
        if r.promedio_grupal >= 80:
            estado = "EXCELENTE"
        elif r.promedio_grupal >= 70:
            estado = "SATISFACTORIO"
        elif r.total_evaluaciones > 0:
            estado = "EN ALERTA"
        else:
            estado = "SIN REGISTROS"
        print(f"{r.id_materia:<8} {r.nombre_materia:<25} {r.total_evaluaciones:<8} {r.promedio_grupal:<13.2f} {r.tasa_aprobacion:<15.1f}% {estado:<15}")
    print("-" * 88)

    con_datos = [r for r in reportes if r.total_evaluaciones > 0]
    if con_datos:
        mejor = max(con_datos, key=lambda x: x.promedio_grupal)
        peor = min(con_datos, key=lambda x: x.promedio_grupal)
        print("INSIGHTS DEL GRUPO:")
        print(f" • Asignatura con mayor rendimiento: {mejor.nombre_materia} ({mejor.promedio_grupal:.2f})")
        print(f" • Asignatura con mayor dificultad:   {peor.nombre_materia} ({peor.promedio_grupal:.2f})")
    print("=" * 88)


def mostrar_consolidado_salon(cons: ConsolidadoSalon) -> None:
    limpiar_pantalla()
    print("=" * 105)
    print("                               CONSOLIDADO GENERAL DEL SALÓN (GRUPO 1)")
    print("=" * 105)
    print(f"{'ID':<10} {'ESTUDIANTE':<24} {'MAT':<7} {'LIT':<7} {'SOC':<7} {'QUI':<7} {'PROG':<7} | {'PROM. FINAL':<12} | {'ESTADO':<12}")
    print("-" * 105)

    for f in cons.filas:
        mat = f"{f.promedios_materias.get('MAT', 0):.1f}" if f.promedios_materias.get('MAT', 0) > 0 else "-"
        lit = f"{f.promedios_materias.get('LIT', 0):.1f}" if f.promedios_materias.get('LIT', 0) > 0 else "-"
        soc = f"{f.promedios_materias.get('SOC', 0):.1f}" if f.promedios_materias.get('SOC', 0) > 0 else "-"
        qui = f"{f.promedios_materias.get('QUI', 0):.1f}" if f.promedios_materias.get('QUI', 0) > 0 else "-"
        prg = f"{f.promedios_materias.get('PROG', 0):.1f}" if f.promedios_materias.get('PROG', 0) > 0 else "-"
        prom = f"{f.promedio_final:.2f}" if f.promedio_final > 0 else "-"
        estado = "APROBADO" if f.aprobado else ("NO APROBADO" if f.promedio_final > 0 else "SIN NOTAS")
        print(f"{f.id_estudiante:<10} {f.nombre_completo[:23]:<24} {mat:<7} {lit:<7} {soc:<7} {qui:<7} {prg:<7} | {prom:<12} | {estado:<12}")

    print("-" * 105)
    print("RESUMEN GLOBAL DEL SALÓN:")
    print(f" • Promedio General del Salón:  {cons.promedio_general_salon:.2f}")
    print(f" • Total de aprendices:          {cons.total_estudiantes}")
    print(f" • Total aprobados:              {cons.total_aprobados} ({cons.tasa_aprobacion:.1f}%)")
    print(f" • Total reprobados:             {cons.total_reprobados}")
    if cons.estudiante_destacado:
        print(f" • Aprendiz con mejor promedio:  {cons.estudiante_destacado} ({cons.mejor_promedio:.2f})")
    print("=" * 105)
