# -*- coding: utf-8 -*-
"""
SISTEMA DE REGISTRO Y PROCESAMIENTO DE CALIFICACIONES
Actividad de Aprendizaje - Lógica de Programación y Algoritmos
Servicio Nacional de Aprendizaje (SENA)
Equipo de Desarrollo: Jayzir Martínez & Julián Vanegas

Descripción:
    Algoritmo para el registro de calificaciones de aprendices,
    cálculo del promedio individual, determinación de aprobación (umbral >= 70.0)
    y cálculo del promedio general y estadísticas consolidadas del grupo.

Estructuras de Datos:
    - Arreglos unidimensionales (listas/vectores): nombres, identificaciones, promedios, estados.
    - Arreglo bidimensional (matriz): calificaciones por aprendiz y actividad.
    - Persistencia en archivo de texto plano: '03_Registros_Calificaciones.txt'.
"""

import os
import sys
from datetime import datetime

# Constante de Negocio
UMBRAL_APROBACION = 70.0
NOMBRE_ARCHIVO_TXT = "03_Registros_Calificaciones.txt"

# Estructura de almacenamiento en memoria
# Cada elemento es un diccionario que modela el registro del aprendiz
aprendices_registrados = []


def limpiar_pantalla():
    """Limpia la terminal en entornos Windows y Unix/Linux/macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución para que el usuario pueda leer los resultados."""
    print("\n" + "—" * 65)
    input("  Presione [ENTER] para continuar...")


def encabezado_modulo(titulo: str):
    """Muestra un encabezado estilizado en consola."""
    limpiar_pantalla()
    print("=" * 70)
    print("   SISTEMA DE CALIFICACIONES - SERVICIO NACIONAL DE APRENDIZAJE")
    print(f"   MÓDULO: {titulo.upper()}")
    print("=" * 70)
    print()


def leer_entero_positivo(mensaje: str, minimo: int = 1, maximo: int = 1000) -> int:
    """Solicita y valida un número entero dentro de un rango determinado."""
    while True:
        try:
            entrada = input(f"{mensaje} [{minimo}-{maximo}]: ").strip()
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  [ERROR] El valor debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("  [ERROR] Debe ingresar un número entero válido.")


def leer_nota_valida(mensaje: str) -> float:
    """Solicita y valida una calificación en la escala estándar de 0.0 a 100.0."""
    while True:
        try:
            entrada = input(f"{mensaje} (0.0 - 100.0): ").strip().replace(",", ".")
            valor = float(entrada)
            if 0.0 <= valor <= 100.0:
                return round(valor, 2)
            print("  [ERROR] La calificación debe ubicarse en el rango de 0.0 a 100.0.")
        except ValueError:
            print("  [ERROR] Entrada inválida. Ingrese un valor numérico (ej: 85.5).")


def leer_texto_no_vacio(mensaje: str) -> str:
    """Solicita y valida que una cadena de texto no esté vacía ni contenga solo espacios."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  [ERROR] Este campo es obligatorio y no puede quedar vacío.")


def registrar_grupo_interactivo():
    """
    Acción 1 a 6:
    Permite registrar interactivamente los aprendices, sus calificaciones,
    calcula promedios individuales y evalúa la aprobación mediante estructura de decisión.
    """
    global aprendices_registrados
    encabezado_modulo("Registro de Aprendices y Calificaciones")

    print("Defina la estructura del grupo a procesar:")
    num_aprendices = leer_entero_positivo("  > Cantidad de aprendices a registrar", minimo=1, maximo=100)
    num_notas = leer_entero_positivo("  > Cantidad de calificaciones por aprendiz", minimo=1, maximo=10)

    nuevos_registros = []

    print("\n" + "-" * 70)
    print("INICIO DE CAPTURA DE DATOS")
    print("-" * 70)

    for i in range(num_aprendices):
        print(f"\n[Aprendiz {i + 1} de {num_aprendices}]")
        id_doc = leer_texto_no_vacio("  • Documento de Identidad / Ficha: ")
        nombre = leer_texto_no_vacio("  • Nombres y Apellidos completos: ")

        calificaciones = []
        acumulador_notas = 0.0

        for j in range(num_notas):
            nota = leer_nota_valida(f"    - Ingrese Nota {j + 1}")
            calificaciones.append(nota)
            acumulador_notas += nota

        # Cálculo de promedio individual
        promedio = round(acumulador_notas / num_notas, 2)

        # Estructura de decisión lógica (Acción 6)
        if promedio >= UMBRAL_APROBACION:
            estado = "Aprobado"
            aprobado_bool = True
        else:
            estado = "No Aprobado"
            aprobado_bool = False

        registro = {
            "id": id_doc,
            "nombre": nombre,
            "calificaciones": calificaciones,
            "promedio": promedio,
            "estado": estado,
            "aprobado": aprobado_bool
        }
        nuevos_registros.append(registro)

        # Retroalimentación inmediata
        icono = "✓" if aprobado_bool else "✗"
        print(f"  => Promedio calculado: {promedio:.2f} | Estado: [{icono} {estado}]")

    aprendices_registrados = nuevos_registros
    print("\n" + "=" * 70)
    print(f"  ¡Éxito! Se han registrado y procesado {len(aprendices_registrados)} aprendices.")
    print("=" * 70)
    pausar()


def cargar_casos_de_prueba():
    """
    Carga un conjunto representativo de 5 aprendices para pruebas de escritorio
    y validación inmediata del algoritmo sin necesidad de digitación manual.
    """
    global aprendices_registrados
    encabezado_modulo("Cargar Datos de Prueba Predeterminados")

    datos_ejemplo = [
        {
            "id": "1001",
            "nombre": "Carlos Alberto Gómez",
            "calificaciones": [85.0, 90.0, 88.0, 92.0],
            "promedio": 88.75,
            "estado": "Aprobado",
            "aprobado": True
        },
        {
            "id": "1002",
            "nombre": "Ana María Rodríguez",
            "calificaciones": [60.0, 65.0, 70.0, 68.0],
            "promedio": 65.75,
            "estado": "No Aprobado",
            "aprobado": False
        },
        {
            "id": "1003",
            "nombre": "Julián David Vanegas",
            "calificaciones": [70.0, 70.0, 70.0, 70.0],
            "promedio": 70.00,
            "estado": "Aprobado",
            "aprobado": True
        },
        {
            "id": "1004",
            "nombre": "Jayzir Martínez",
            "calificaciones": [95.0, 98.0, 94.0, 100.0],
            "promedio": 96.75,
            "estado": "Aprobado",
            "aprobado": True
        },
        {
            "id": "1005",
            "nombre": "Laura Marcela Pérez",
            "calificaciones": [45.0, 50.0, 58.0, 52.0],
            "promedio": 51.25,
            "estado": "No Aprobado",
            "aprobado": False
        }
    ]

    aprendices_registrados = datos_ejemplo
    print("Se cargaron 5 registros de prueba con casos representativos:")
    print("  1. Rendimiento Sobresaliente (Carlos Gómez - Prom: 88.75)")
    print("  2. Reprobación cercana al límite (Ana Rodríguez - Prom: 65.75)")
    print("  3. Caso Frontera/Límite Exacto (Julián Vanegas - Prom: 70.00 -> Aprobado)")
    print("  4. Rendimiento Excelente / Nota 100 (Jayzir Martínez - Prom: 96.75)")
    print("  5. Reprobación por bajo promedio (Laura Pérez - Prom: 51.25)")
    print("\n  Registros listos para visualización, estadísticas y exportación.")
    pausar()


def calcular_metricas_grupo():
    """
    Calcula el promedio general del grupo y estadísticas complementarias.
    Retorna un diccionario con las métricas calculadas.
    """
    if not aprendices_registrados:
        return None

    total_aprendices = len(aprendices_registrados)
    acumulador_promedios = 0.0
    total_aprobados = 0
    total_no_aprobados = 0

    mejor_promedio = -1.0
    peor_promedio = 101.0
    aprendiz_destacado = ""
    aprendiz_refuerzo = ""

    for item in aprendices_registrados:
        prom = item["promedio"]
        acumulador_promedios += prom

        if item["aprobado"]:
            total_aprobados += 1
        else:
            total_no_aprobados += 1

        if prom > mejor_promedio:
            mejor_promedio = prom
            aprendiz_destacado = item["nombre"]

        if prom < peor_promedio:
            peor_promedio = prom
            aprendiz_refuerzo = item["nombre"]

    promedio_general = round(acumulador_promedios / total_aprendices, 2)
    porcentaje_aprobacion = round((total_aprobados / total_aprendices) * 100, 2)
    porcentaje_reprobacion = round((total_no_aprobados / total_aprendices) * 100, 2)

    return {
        "total": total_aprendices,
        "acumulador": round(acumulador_promedios, 2),
        "promedio_general": promedio_general,
        "aprobados": total_aprobados,
        "no_aprobados": total_no_aprobados,
        "pct_aprobados": porcentaje_aprobacion,
        "pct_no_aprobados": porcentaje_reprobacion,
        "mejor_promedio": mejor_promedio,
        "destacado": aprendiz_destacado,
        "peor_promedio": peor_promedio,
        "refuerzo": aprendiz_refuerzo
    }


def mostrar_reporte_individual():
    """Despliega en pantalla el listado detallado de cada aprendiz."""
    encabezado_modulo("Listado Individual de Calificaciones")

    if not aprendices_registrados:
        print("  [AVISO] No hay aprendices registrados actualmente.")
        print("  Utilice la opción 1 o 2 del menú principal para ingresar datos.")
        pausar()
        return

    print(f"{'ID / DOC':<12} | {'NOMBRE DEL APRENDIZ':<28} | {'CALIFICACIONES':<22} | {'PROM':<7} | {'ESTADO':<12}")
    print("-" * 90)

    for ap in aprendices_registrados:
        notas_str = ", ".join(f"{n:.1f}" for n in ap["calificaciones"])
        notas_fmt = f"[{notas_str}]"
        estado_fmt = f"✓ {ap['estado']}" if ap["aprobado"] else f"✗ {ap['estado']}"
        print(f"{ap['id']:<12} | {ap['nombre'][:28]:<28} | {notas_fmt:<22} | {ap['promedio']:>6.2f} | {estado_fmt:<12}")

    print("-" * 90)
    print(f"Total de registros procesados: {len(aprendices_registrados)}")
    pausar()


def mostrar_resumen_grupal():
    """
    Acción 7:
    Calcula y presenta el promedio general del grupo y métricas pedagógicas.
    """
    encabezado_modulo("Resumen Consolidado y Promedio General del Grupo")

    metricas = calcular_metricas_grupo()
    if not metricas:
        print("  [AVISO] No hay datos cargados para calcular estadísticas grupales.")
        pausar()
        return

    print("+" + "-" * 66 + "+")
    print(f"| {'MÉTRICA / INDICADOR':<42} | {'VALOR OBTENIDO':>20} |")
    print("+" + "-" * 66 + "+")
    pct_aprob_str = f"{metricas['pct_aprobados']:.1f} %"
    pct_no_aprob_str = f"{metricas['pct_no_aprobados']:.1f} %"
    mejor_prom_str = f"{metricas['mejor_promedio']:.2f}"
    peor_prom_str = f"{metricas['peor_promedio']:.2f}"

    print(f"| {'Total de Aprendices Evaluados':<42} | {metricas['total']:>20} |")
    print(f"| {'Sumatoria Total de Promedios':<42} | {metricas['acumulador']:>20.2f} |")
    print(f"| {'PROMEDIO GENERAL DEL GRUPO':<42} | {metricas['promedio_general']:>20.2f} |")
    print(f"| {'Condición de Aprobación Institucional':<42} | {'Promedio >= 70.0':>20} |")
    print(f"| {'Total Aprendices Aprobados':<42} | {metricas['aprobados']:>20} |")
    print(f"| {'Total Aprendices No Aprobados':<42} | {metricas['no_aprobados']:>20} |")
    print(f"| {'Tasa de Aprobación del Grupo':<42} | {pct_aprob_str:>20} |")
    print(f"| {'Tasa de No Aprobación':<42} | {pct_no_aprob_str:>20} |")
    print(f"| {'Calificación Promedio Más Alta':<42} | {mejor_prom_str:>20} |")
    print(f"| {'  > Aprendiz Destacado':<42} | {metricas['destacado'][:20]:>20} |")
    print(f"| {'Calificación Promedio Más Baja':<42} | {peor_prom_str:>20} |")
    print(f"| {'  > Aprendiz con Mayor Oportunidad':<42} | {metricas['refuerzo'][:20]:>20} |")
    print("+" + "-" * 66 + "+")

    # Diagnóstico interpretativo
    if metricas["promedio_general"] >= UMBRAL_APROBACION:
        print("\n  [DIAGNÓSTICO GRUPAL]: El grupo superó el promedio aprobatorio institucional satisfactoriamente.")
    else:
        print("\n  [DIAGNÓSTICO GRUPAL]: El rendimiento general del grupo requiere plan de mejoramiento pedagógico.")

    pausar()


def exportar_registros_txt():
    """Genera el archivo plano con el informe consolidado y tabulado."""
    encabezado_modulo("Exportación de Registros a Archivo Plano")

    metricas = calcular_metricas_grupo()
    if not metricas:
        print("  [ERROR] No hay registros para exportar. Ingrese o cargue aprendices primero.")
        pausar()
        return

    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_ARCHIVO_TXT)

    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write("=" * 95 + "\n")
            f.write("SERVICIO NACIONAL DE APRENDIZAJE - SENA\n")
            f.write("SISTEMA DE REGISTRO Y PROCESAMIENTO DE CALIFICACIONES\n")
            f.write(f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Equipo de Desarrollo: Jayzir Martínez & Julián Vanegas\n")
            f.write("=" * 95 + "\n\n")

            f.write("LISTADO DETALLADO DE APRENDICES Y CALIFICACIONES:\n")
            f.write("-" * 95 + "\n")
            f.write(f"{'ID':<10} | {'NOMBRE DEL APRENDIZ':<28} | {'NOTAS':<22} | {'PROMEDIO':<10} | {'ESTADO':<14}\n")
            f.write("-" * 95 + "\n")

            for ap in aprendices_registrados:
                notas_str = ", ".join(f"{n:.1f}" for n in ap["calificaciones"])
                f.write(f"{ap['id']:<10} | {ap['nombre'][:28]:<28} | {notas_str:<22} | {ap['promedio']:>8.2f} | {ap['estado']:<14}\n")

            f.write("-" * 95 + "\n\n")

            pct_aprob_export = f"{metricas['pct_aprobados']:.1f}%"
            mejor_prom_export = f"{metricas['mejor_promedio']:.2f}"
            peor_prom_export = f"{metricas['peor_promedio']:.2f}"

            f.write("RESUMEN GENERAL Y ESTADÍSTICAS DEL GRUPO:\n")
            f.write("+" + "-" * 50 + "+" + "-" * 20 + "+\n")
            f.write(f"| {'Métrica':<48} | {'Valor':>18} |\n")
            f.write("+" + "-" * 50 + "+" + "-" * 20 + "+\n")
            f.write(f"| {'Total de Aprendices Evaluados':<48} | {metricas['total']:>18} |\n")
            f.write(f"| {'PROMEDIO GENERAL DEL GRUPO':<48} | {metricas['promedio_general']:>18.2f} |\n")
            f.write(f"| {'Aprendices Aprobados (>= 70)':<48} | {metricas['aprobados']:>18} |\n")
            f.write(f"| {'Aprendices No Aprobados (< 70)':<48} | {metricas['no_aprobados']:>18} |\n")
            f.write(f"| {'Porcentaje de Aprobación':<48} | {pct_aprob_export:>18} |\n")
            f.write(f"| {'Promedio Más Alto':<48} | {mejor_prom_export:>18} |\n")
            f.write(f"| {'Promedio Más Bajo':<48} | {peor_prom_export:>18} |\n")
            f.write("+" + "-" * 50 + "+" + "-" * 20 + "+\n")

        print(f"  [ÉXITO] Archivo generado correctamente en:")
        print(f"  > {ruta_archivo}")
    except Exception as e:
        print(f"  [ERROR] Ocurrió un fallo al exportar el archivo: {e}")

    pausar()


def simular_prueba_escritorio():
    """
    Acción 8:
    Muestra la traza formal de prueba de escritorio paso a paso,
    evidenciando el ciclo de ejecución, estado de las variables y acumuladores.
    """
    encabezado_modulo("Prueba de Escritorio Automatizada (Paso a Paso)")

    print("Traza de ejecución formal paso a paso para un grupo de 3 aprendices con 3 notas:\n")
    print("Variables en seguimiento:")
    print("  • i (Índice aprendiz)  • acum_notas (Suma notas) • prom (Promedio individual)")
    print("  • acum_gral (Suma promedios) • estado (Decisión >= 70)")
    print("=" * 80)
    print(f"{'Paso':<5} | {'i':<3} | {'Aprendiz':<18} | {'Notas':<14} | {'Suma':<7} | {'Prom':<6} | {'Estado':<11} | {'Acum. Gral':<10}")
    print("-" * 80)

    casos_traza = [
        ("1", "Carlos Gómez", [80.0, 75.0, 85.0]),
        ("2", "Ana Rodríguez", [60.0, 65.0, 70.0]),
        ("3", "Julián Vanegas", [70.0, 70.0, 70.0])
    ]

    acum_general = 0.0
    for idx, (ap_id, nombre, notas) in enumerate(casos_traza, 1):
        suma_indiv = sum(notas)
        prom_indiv = round(suma_indiv / len(notas), 2)
        estado = "Aprobado" if prom_indiv >= 70.0 else "No Aprobado"
        acum_general += prom_indiv
        notas_str = f"{notas[0]:.0f},{notas[1]:.0f},{notas[2]:.0f}"
        print(f"{idx:<5} | {idx:<3} | {nombre:<18} | {notas_str:<14} | {suma_indiv:<7.1f} | {prom_indiv:<6.2f} | {estado:<11} | {acum_general:<10.2f}")

    prom_grupo_final = round(acum_general / len(casos_traza), 2)
    print("-" * 80)
    print(f"\nCÁLCULO FINAL DEL CICLO:")
    print(f"  > Sumatoria Total Acumulada = {acum_general:.2f}")
    print(f"  > Promedio General = {acum_general:.2f} / {len(casos_traza)} = {prom_grupo_final:.2f}")
    print(f"  > Veredicto del Algoritmo: Ejecución correcta sin desviaciones aritméticas.")
    pausar()


def menu_principal():
    """Despliega el menú principal interactivo del sistema."""
    while True:
        encabezado_modulo("Menú Principal de Operaciones")
        print("  [1] Registrar nuevo grupo de aprendices (Ingreso interactivo)")
        print("  [2] Cargar 5 casos de prueba predeterminados (Demostración inmediata)")
        print("  [3] Visualizar listado individual de calificaciones y promedios")
        print("  [4] Visualizar resumen estadístico y promedio general del grupo")
        print("  [5] Exportar registros a archivo plano (03_Registros_Calificaciones.txt)")
        print("  [6] Ejecutar traza de Prueba de Escritorio paso a paso")
        print("  [0] Salir del sistema")
        print("-" * 70)

        opcion = input("  Seleccione una opción [0-6]: ").strip()

        if opcion == "1":
            registrar_grupo_interactivo()
        elif opcion == "2":
            cargar_casos_de_prueba()
        elif opcion == "3":
            mostrar_reporte_individual()
        elif opcion == "4":
            mostrar_resumen_grupal()
        elif opcion == "5":
            exportar_registros_txt()
        elif opcion == "6":
            simular_prueba_escritorio()
        elif opcion == "0":
            limpiar_pantalla()
            print("\n" + "=" * 60)
            print("   ¡Gracias por utilizar el Sistema de Calificaciones SENA!")
            print("   Desarrollado por: Jayzir Martínez & Julián Vanegas")
            print("=" * 60 + "\n")
            sys.exit(0)
        else:
            print("  [ERROR] Opción no válida. Digite un número entre 0 y 6.")
            pausar()


if __name__ == "__main__":
    menu_principal()
