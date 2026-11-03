import os

# Constantes
PRECIO_BOTELLA = 2500
PRECIO_FRUTA = 1800
UMBRAL_DESCUENTO = 10000
VALOR_DESCUENTO = 1000

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo (Windows o Unix/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_compra(cantidad_botellas: int, cantidad_frutas: int):
    # Proceso
    costo_botellas = cantidad_botellas * PRECIO_BOTELLA
    costo_frutas = cantidad_frutas * PRECIO_FRUTA
    subtotal = costo_botellas + costo_frutas
    
    # Descuento acumulativo: $1.000 por cada $10.000 en el subtotal
    veces_descuento = subtotal // UMBRAL_DESCUENTO
    descuento_aplicado = veces_descuento * VALOR_DESCUENTO
        
    total_pagar = subtotal - descuento_aplicado
    
    # Salida
    print("\n--- RESUMEN DE LA COMPRA ---")
    print(f"Botellas ({cantidad_botellas} x ${PRECIO_BOTELLA:,}): ${costo_botellas:,}")
    print(f"Frutas ({cantidad_frutas} x ${PRECIO_FRUTA:,}):   ${costo_frutas:,}")
    print(f"Subtotal:       ${subtotal:,}")
    if veces_descuento > 0:
        print(f"Descuento ({veces_descuento}x ${VALOR_DESCUENTO:,}): -${descuento_aplicado:,}")
    else:
        print(f"Descuento:      $0")
    print(f"Total a pagar:  ${total_pagar:,}")
    print("-" * 35)

def pedir_cantidad(mensaje: str) -> int:
    """Solicita un número entero positivo o cero con validación de errores."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("❌ Por favor, ingrese un número mayor o igual a 0.")
                continue
            return valor
        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido.")

def menu():
    """Menú interactivo en consola."""
    while True:
        print("=" * 35)
        print("   MENÚ - COMPRA PAUSA ACTIVA")
        print("=" * 35)
        print("1. Calcular nueva compra")
        print("2. Ver casos de ejemplo")
        print("3. Salir")
        print("=" * 35)
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        limpiar_pantalla()
        
        if opcion == "1":
            print("=== CALCULAR NUEVA COMPRA ===\n")
            botellas = pedir_cantidad("Cantidad de botellas de agua: ")
            frutas = pedir_cantidad("Cantidad de frutas: ")
            calcular_compra(botellas, frutas)
            input("\nPresione Enter para volver al menú...")
            limpiar_pantalla()
            
        elif opcion == "2":
            print("=== CASOS DE EJEMPLO ===\n")
            print("Caso 1 (3 botellas, 2 frutas -> Subtotal $11.100):")
            calcular_compra(cantidad_botellas=3, cantidad_frutas=2)
            
            print("\nCaso 2 (2 botellas, 1 fruta -> Subtotal $6.800):")
            calcular_compra(cantidad_botellas=2, cantidad_frutas=1)

            print("\nCaso 3 (6 botellas, 4 frutas -> Subtotal $22.200):")
            calcular_compra(cantidad_botellas=6, cantidad_frutas=4)
            input("\nPresione Enter para volver al menú...")
            limpiar_pantalla()
            
        elif opcion == "3":
            print("¡Gracias por utilizar el sistema! Hasta pronto.\n")
            break
            
        else:
            print("⚠️   Opción no válida. Por favor elija 1, 2 o 3.\n")

