# -*- coding: utf-8 -*-
"""
MÓDULO DE NÓMINA - TRANSCARIBECOL S.C.A.
Actividad 3.4: Reto de Desarrollo en Parejas
Desarrolladores: Julián Vanegas & Jayzir Martínez
Apegado 100% a la Legislación Laboral Colombiana (CST, Ley 100 de 1993, Decreto 1072 de 2015).

Estructura de Datos:
    Matriz de registros (lista de diccionarios / listas) en memoria.
Persistencia:
    Generación y lectura en archivo de texto plano (.TXT).
"""

import os
import sys

# Constantes de Negocio y Normativas
VALOR_HORA_ADMIN = 20000.0
VALOR_HORA_EXTRA_ADMIN = 25000.0
ARL_TASA_RIESGO_I = 0.00522    # 0.522%

VALOR_HORA_OPERATIVO = 40000.0
PORCENTAJE_IBC_OPS = 0.40       # 40% del valor mensual bruto (Art. 244 Ley 1955 de 2019)
SALUD_TASA_OPS = 0.125          # 12.5% integral a cargo del contratista
PENSION_TASA_OPS = 0.160        # 16.0% integral a cargo del contratista

# Tasas dependientes (Administrativo - Código Sustantivo del Trabajo)
SALUD_TASA_DEPENDIENTE = 0.04   # 4% a cargo del trabajador
PENSION_TASA_DEPENDIENTE = 0.04 # 4% a cargo del trabajador

# Parámetros por cargo operativo según guía
CARGOS_OPERATIVOS = {
    "1": {
        "nombre": "Conductor",
        "horas": 160,
        "arl_tasa": 0.01044,    # Riesgo II: 1.044%
        "riesgo_nombre": "Riesgo II (1.044%)"
    },
    "2": {
        "nombre": "Oficios Generales",
        "horas": 100,
        "arl_tasa": 0.00522,    # Riesgo I: 0.522%
        "riesgo_nombre": "Riesgo I (0.522%)"
    },
    "3": {
        "nombre": "Vigilancia",
        "horas": 336,
        "arl_tasa": 0.04350,    # Riesgo IV: 4.350%
        "riesgo_nombre": "Riesgo IV (4.350%)"
    }
}

ARCHIVO_SALIDA = "03_Registros_Nomina.txt"

# Estructura en memoria: Lista de registros procesados
registros_nomina = []


def limpiar_pantalla():
    """Limpia la consola de manera compatible con Windows, Linux y macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución para que el usuario pueda leer los resultados antes de limpiar."""
    print()
    input("Presione ENTER para continuar...")


def formatear_moneda(valor: float) -> str:
    """Formatea un valor numérico a moneda colombiana sin decimales."""
    return f"${valor:,.0f}".replace(",", ".")


def calcular_administrativo(nombre: str, cedula: str, cargo: str, horas_trabajadas: float, horas_extras: float) -> dict:
    """
    Liquida la nómina para un empleado administrativo bajo contrato de trabajo (CST).
    - Salario base = HT * 20.000
    - TPHE = HE * 25.000
    - Total Devengado = Salario base + TPHE
    - Deducciones trabajador: Salud (4%) y Pensión (4%)
    - ARL: Riesgo I (0.522%), a cargo del empleador (informativo legal)
    - Total Neto a pagar = Total Devengado - (Salud + Pensión)
    """
    salario_base = horas_trabajadas * VALOR_HORA_ADMIN
    tphe = horas_extras * VALOR_HORA_EXTRA_ADMIN
    total_devengado = salario_base + tphe

    salud_trabajador = total_devengado * SALUD_TASA_DEPENDIENTE
    pension_trabajador = total_devengado * PENSION_TASA_DEPENDIENTE
    arl_empleador = total_devengado * ARL_TASA_RIESGO_I

    total_deducciones = salud_trabajador + pension_trabajador
    total_a_pagar = total_devengado - total_deducciones

    return {
        "nombre": nombre,
        "cedula": cedula,
        "tipo": "Administrativo",
        "cargo": cargo,
        "ht": horas_trabajadas,
        "salario": salario_base,
        "he": horas_extras,
        "tphe": tphe,
        "ibc": total_devengado,
        "salud": salud_trabajador,
        "pension": pension_trabajador,
        "arl": arl_empleador,
        "arl_a_cargo": "Empleador (informativo)",
        "total_devengado": total_devengado,
        "total_deducciones": total_deducciones,
        "total_a_pagar": total_a_pagar
    }


def calcular_operativo(nombre: str, cedula: str, codigo_cargo: str) -> dict:
    """
    Liquida los honorarios de personal operativo bajo contrato de prestación de servicios (OPS).
    - Tarifa: $40.000 / hora
    - HT fijas según cargo: Conductor (160h), Oficios Generales (100h), Vigilancia (336h)
    - Bruto (Honorarios) = HT * 40.000
    - IBC = 40% del Bruto
    - Deducciones contratista: Salud (12.5% de IBC), Pensión (16% de IBC), ARL (según riesgo sobre IBC)
    - Total Neto a pagar = Bruto - (Salud + Pensión + ARL)
    """
    cargo_info = CARGOS_OPERATIVOS[codigo_cargo]
    cargo_nombre = cargo_info["nombre"]
    horas_mes = cargo_info["horas"]
    arl_tasa = cargo_info["arl_tasa"]

    salario_bruto = horas_mes * VALOR_HORA_OPERATIVO
    he = 0.0
    tphe = 0.0

    ibc = salario_bruto * PORCENTAJE_IBC_OPS
    salud = ibc * SALUD_TASA_OPS
    pension = ibc * PENSION_TASA_OPS
    arl = ibc * arl_tasa

    total_deducciones = salud + pension + arl
    total_a_pagar = salario_bruto - total_deducciones

    return {
        "nombre": nombre,
        "cedula": cedula,
        "tipo": "Operativo",
        "cargo": cargo_nombre,
        "ht": float(horas_mes),
        "salario": salario_bruto,
        "he": he,
        "tphe": tphe,
        "ibc": ibc,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "arl_a_cargo": "Contratista (deducción)",
        "total_devengado": salario_bruto,
        "total_deducciones": total_deducciones,
        "total_a_pagar": total_a_pagar
    }


def mostrar_comprobante_pantalla(reg: dict):
    """Muestra en consola el comprobante individual de liquidación."""
    print("\n" + "=" * 65)
    print("      TRANSCARIBECOL S.C.A. - COMPROBANTE DE PAGO")
    print("=" * 65)
    print(f" Empleado:       {reg['nombre']}")
    print(f" Cédula / ID:    {reg['cedula']}")
    print(f" Tipo Personal:  {reg['tipo']}")
    print(f" Cargo:          {reg['cargo']}")
    print("-" * 65)
    print(" CONCEPTO DEVENGADOS                        HORAS       VALOR")
    print(f"  Horas Ordinarias ({formatear_moneda(VALOR_HORA_ADMIN if reg['tipo']=='Administrativo' else VALOR_HORA_OPERATIVO)}/h)     {reg['ht']:>6.1f}   {formatear_moneda(reg['salario']):>12}")
    if reg['tipo'] == 'Administrativo' and reg['he'] > 0:
        print(f"  Horas Extras ($25.000/h)                 {reg['he']:>6.1f}   {formatear_moneda(reg['tphe']):>12}")
    print(f"  TOTAL DEVENGADO / HONORARIOS:                         {formatear_moneda(reg['total_devengado']):>12}")
    print("-" * 65)
    print(f" BASE DE COTIZACIÓN (IBC):                              {formatear_moneda(reg['ibc']):>12}")
    print(" CONCEPTO DEDUCCIONES                                   VALOR")
    if reg['tipo'] == 'Administrativo':
        print(f"  Aporte Salud (4% a cargo trabajador):                 {formatear_moneda(reg['salud']):>12}")
        print(f"  Aporte Pensión (4% a cargo trabajador):               {formatear_moneda(reg['pension']):>12}")
        print(f"  * ARL Riesgo I (0.522% a cargo patronal):             {formatear_moneda(reg['arl']):>12} [Aporte Empresa]")
    else:
        print(f"  Aporte Salud (12.5% sobre IBC):                       {formatear_moneda(reg['salud']):>12}")
        print(f"  Aporte Pensión (16.0% sobre IBC):                     {formatear_moneda(reg['pension']):>12}")
        print(f"  Aporte ARL ({reg['cargo']} sobre IBC):                  {formatear_moneda(reg['arl']):>12}")
    print(f"  TOTAL DEDUCCIONES AL TRABAJADOR:                      {formatear_moneda(reg['total_deducciones']):>12}")
    print("=" * 65)
    print(f"  TOTAL NETO A PAGAR:                                   {formatear_moneda(reg['total_a_pagar']):>12}")
    print("=" * 65 + "\n")


def guardar_registros_txt(archivo: str = ARCHIVO_SALIDA):
    """Exporta todos los registros en memoria hacia el archivo TXT según la tabla de la guía."""
    if not registros_nomina:
        print("\n[!] No hay registros para guardar. Ingrese trabajadores primero.")
        return

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("=" * 135 + "\n")
        f.write("                TRANSCARIBECOL S.C.A. - REGISTRO GENERAL DE NÓMINA Y HONORARIOS\n")
        f.write("                       Cumplimiento Código Sustantivo del Trabajo y Ley 100\n")
        f.write("                     Elaborado por: Julián Vanegas & Jayzir Martínez (SENA)\n")
        f.write("=" * 135 + "\n")
        
        encabezado = f"{'Nombre':<20} | {'Tipo':<14} | {'Cargo':<18} | {'HT':>5} | {'Salario':>12} | {'HE':>4} | {'TPHE':>11} | {'Salud':>10} | {'Pensión':>10} | {'ARL':>10} | {'Total a pagar':>14}\n"
        f.write(encabezado)
        f.write("-" * 135 + "\n")

        total_salarios = 0.0
        total_tphe = 0.0
        total_salud = 0.0
        total_pension = 0.0
        total_arl = 0.0
        gran_total_neto = 0.0

        for r in registros_nomina:
            linea = (
                f"{r['nombre']:<20} | "
                f"{r['tipo']:<14} | "
                f"{r['cargo']:<18} | "
                f"{r['ht']:>5.0f} | "
                f"{formatear_moneda(r['salario']):>12} | "
                f"{r['he']:>4.0f} | "
                f"{formatear_moneda(r['tphe']):>11} | "
                f"{formatear_moneda(r['salud']):>10} | "
                f"{formatear_moneda(r['pension']):>10} | "
                f"{formatear_moneda(r['arl']):>10} | "
                f"{formatear_moneda(r['total_a_pagar']):>14}\n"
            )
            f.write(linea)

            total_salarios += r['salario']
            total_tphe += r['tphe']
            total_salud += r['salud']
            total_pension += r['pension']
            total_arl += r['arl']
            gran_total_neto += r['total_a_pagar']

        f.write("-" * 135 + "\n")
        totales = (
            f"{'TOTALES':<20} | "
            f"{'-':<14} | "
            f"{'-':<18} | "
            f"{'-':>5} | "
            f"{formatear_moneda(total_salarios):>12} | "
            f"{'-':>4} | "
            f"{formatear_moneda(total_tphe):>11} | "
            f"{formatear_moneda(total_salud):>10} | "
            f"{formatear_moneda(total_pension):>10} | "
            f"{formatear_moneda(total_arl):>10} | "
            f"{formatear_moneda(gran_total_neto):>14}\n"
        )
        f.write(totales)
        f.write("=" * 135 + "\n")
        f.write(f"Total registros procesados: {len(registros_nomina)}\n")
        f.write("* Nota Legal: Para personal Administrativo, el valor de ARL indicado corresponde al aporte patronal obligatorio por ley.\n")

    print(f"\n[OK] Se han guardado satisfactoriamente {len(registros_nomina)} registros en: {archivo}")


def listar_resumen_pantalla():
    """Presenta en consola la tabla consolidada de todos los trabajadores procesados."""
    if not registros_nomina:
        print("\n[!] Aún no hay empleados registrados.")
        return

    print("\n" + "=" * 135)
    print("                                   RESUMEN GENERAL DE NÓMINA - TRANSCARIBECOL")
    print("=" * 135)
    print(f"{'Nombre':<20} | {'Tipo':<14} | {'Cargo':<18} | {'HT':>5} | {'Salario':>12} | {'HE':>4} | {'TPHE':>11} | {'Salud':>10} | {'Pensión':>10} | {'ARL':>10} | {'Total a pagar':>14}")
    print("-" * 135)
    for r in registros_nomina:
        print(
            f"{r['nombre']:<20} | "
            f"{r['tipo']:<14} | "
            f"{r['cargo']:<18} | "
            f"{r['ht']:>5.0f} | "
            f"{formatear_moneda(r['salario']):>12} | "
            f"{r['he']:>4.0f} | "
            f"{formatear_moneda(r['tphe']):>11} | "
            f"{formatear_moneda(r['salud']):>10} | "
            f"{formatear_moneda(r['pension']):>10} | "
            f"{formatear_moneda(r['arl']):>10} | "
            f"{formatear_moneda(r['total_a_pagar']):>14}"
        )
    print("=" * 135 + "\n")


def leer_archivo_txt(archivo: str = ARCHIVO_SALIDA):
    """Muestra el contenido actual del archivo .TXT generado."""
    if not os.path.exists(archivo):
        print(f"\n[!] El archivo '{archivo}' aún no existe. Genérelo primero desde la opción correspondiente.")
        return

    print(f"\n--- CONTENIDO DEL ARCHIVO {archivo} ---")
    with open(archivo, "r", encoding="utf-8") as f:
        print(f.read())


def registrar_trabajador():
    """Flujo interactivo para captura de datos y validaciones de un nuevo empleado."""
    limpiar_pantalla()
    print("=" * 60)
    print("              REGISTRAR NUEVO TRABAJADOR")
    print("=" * 60)
    nombre = input("Ingrese el nombre completo: ").strip()
    while not nombre:
        print("[!] El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre completo: ").strip()

    cedula = input("Ingrese el documento / cédula: ").strip()
    while not cedula:
        print("[!] La cédula no puede estar vacía.")
        cedula = input("Ingrese el documento / cédula: ").strip()

    print("\nSeleccione el tipo de personal:")
    print("  1. Administrativo (Contrato Laboral CST - $20.000/h, HE $25.000/h)")
    print("  2. Operativo (Prestación de Servicios - $40.000/h, IBC 40%)")
    tipo_opcion = input("Opción (1 o 2): ").strip()
    while tipo_opcion not in ["1", "2"]:
        print("[!] Opción inválida. Digite 1 o 2.")
        tipo_opcion = input("Opción (1 o 2): ").strip()

    if tipo_opcion == "1":
        # Administrativo
        cargo = input("Ingrese el cargo administrativo (ej. Auxiliar Contable, Asistente, Coordinador): ").strip()
        if not cargo:
            cargo = "Asistente Administrativo"

        while True:
            try:
                ht = float(input("Ingrese las horas ordinarias laboradas en el mes: ").strip())
                if ht < 0:
                    print("[!] Las horas no pueden ser negativas.")
                    continue
                break
            except ValueError:
                print("[!] Ingrese un valor numérico válido.")

        while True:
            try:
                he = float(input("Ingrese las horas extras laboradas (0 si no aplica): ").strip())
                if he < 0:
                    print("[!] Las horas extras no pueden ser negativas.")
                    continue
                break
            except ValueError:
                print("[!] Ingrese un valor numérico válido.")

        registro = calcular_administrativo(nombre, cedula, cargo, ht, he)

    else:
        # Operativo
        print("\nSeleccione el cargo operativo:")
        print("  1. Conductor          (160 h mensuales - ARL Riesgo II 1.044%)")
        print("  2. Oficios Generales  (100 h mensuales - ARL Riesgo I 0.522%)")
        print("  3. Vigilancia         (336 h mensuales - ARL Riesgo IV 4.350%)")
        cargo_cod = input("Seleccione el cargo (1, 2 o 3): ").strip()
        while cargo_cod not in ["1", "2", "3"]:
            print("[!] Opción inválida. Seleccione 1, 2 o 3.")
            cargo_cod = input("Seleccione el cargo (1, 2 o 3): ").strip()

        registro = calcular_operativo(nombre, cedula, cargo_cod)

    # Almacenar en la estructura en memoria
    registros_nomina.append(registro)

    # Mostrar comprobante inmediato en pantalla
    mostrar_comprobante_pantalla(registro)
    print("[OK] Trabajador liquidado y registrado en memoria correctamente.")


def precargar_casos_estudio():
    """Carga los 4 casos de prueba obligatorios de la guía para pruebas inmediatas."""
    global registros_nomina
    registros_nomina = [
        calcular_administrativo("Carlos Mendoza", "1045236891", "Asistente Contable", 160.0, 10.0),
        calcular_operativo("Andrés Restrepo", "1018452390", "1"),  # Conductor
        calcular_operativo("María Gómez", "1023984125", "2"),      # Oficios Generales
        calcular_operativo("Jorge Morales", "1032541890", "3")      # Vigilancia
    ]
    print(f"\n[OK] Se han precargado los 4 casos de prueba oficiales de la guía ({len(registros_nomina)} trabajadores).")


def menu():
    """Función principal con el bucle de interacción del usuario."""
    while True:
        limpiar_pantalla()
        print("=" * 55)
        print("        SISTEMA DE NÓMINA - TRANSCARIBECOL S.C.A.")
        print("      Cumplimiento Laboral CST y Ley 100 de 1993")
        print("         Equipo: Julián Vanegas & Jayzir Martínez")
        print("=" * 55)
        print("  1. Registrar nuevo trabajador y calcular nómina")
        print("  2. Mostrar resumen consolidado en pantalla")
        print("  3. Guardar registros en archivo TXT")
        print("  4. Consultar archivo TXT existente")
        print("  5. Cargar los 4 casos de prueba oficiales de la guía")
        print("  6. Salir")
        print("=" * 55)
        print(f" Registros en memoria: {len(registros_nomina)}")
        print("=" * 55)
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            registrar_trabajador()
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            listar_resumen_pantalla()
            pausar()
        elif opcion == "3":
            limpiar_pantalla()
            guardar_registros_txt()
            pausar()
        elif opcion == "4":
            limpiar_pantalla()
            leer_archivo_txt()
            pausar()
        elif opcion == "5":
            limpiar_pantalla()
            precargar_casos_estudio()
            pausar()
        elif opcion == "6":
            limpiar_pantalla()
            print("=" * 55)
            print("  ¡Gracias por utilizar el Módulo de Nómina de")
            print("         TransCaribeCol S.C.A.! Hasta pronto.")
            print("=" * 55 + "\n")
            sys.exit(0)
        else:
            print("\n[!] Opción no válida. Por favor digite un número del 1 al 6.")
            pausar()


if __name__ == "__main__":
    menu()
