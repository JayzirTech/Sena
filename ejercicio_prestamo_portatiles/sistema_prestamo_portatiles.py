"""
Sistema de Préstamo de Computadores Portátiles
Consola interactiva - Almacenamiento local en memoria (sin dependencias externas).
"""

from datetime import datetime, timedelta
import os
import sys

# Compatibilidad con codificación UTF-8 en consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==============================================================================
# BASE DE DATOS LOCAL EN MEMORIA (CÓDIGOS MERAMENTE NUMÉRICOS)
# ==============================================================================
equipos = {
    "1": {"modelo": "Dell Latitude 5420", "estado": "Disponible"},
    "2": {"modelo": "Lenovo ThinkPad E14", "estado": "Disponible"},
    "3": {"modelo": "HP ProBook 450", "estado": "Disponible"},
    "4": {"modelo": "MacBook Air M1", "estado": "En revisión técnica"},
}

usuarios = {
    "101": {"nombre": "Carlos Gómez", "sancionado": False},
    "102": {"nombre": "Ana Rodríguez", "sancionado": False},
    "103": {"nombre": "Pedro Morales", "sancionado": True},  # Caso de prueba 2: Sancionado
}

prestamos = []  # Historial y préstamos activos


def buscar_equipo(id_ingresado):
    """Busca y normaliza el ID de un equipo soportando números directos o prefijos."""
    id_limpio = id_ingresado.strip()
    if id_limpio in equipos:
        return id_limpio
    # Soporte para ceros a la izquierda (ej: '01' -> '1')
    sin_ceros = id_limpio.lstrip("0")
    if sin_ceros in equipos:
        return sin_ceros
    # Compatibilidad con formato anterior (ej: 'PORT-01' -> '1')
    if id_limpio.upper().startswith("PORT-"):
        num = id_limpio.upper().replace("PORT-", "").lstrip("0")
        if num in equipos:
            return num
    return None


def buscar_usuario(id_ingresado):
    """Busca y normaliza el ID de un usuario soportando números directos o atajos."""
    id_limpio = id_ingresado.strip()
    if id_limpio in usuarios:
        return id_limpio
    # Atajo rápido: si se ingresa 1, 2 o 3 se mapea al usuario 101, 102 o 103
    if id_limpio in ("1", "2", "3") and f"10{id_limpio}" in usuarios:
        return f"10{id_limpio}"
    # Compatibilidad con formato anterior (ej: 'USR-01' -> '101')
    if id_limpio.upper().startswith("USR-"):
        num = id_limpio.upper().replace("USR-", "").lstrip("0")
        if f"10{num}" in usuarios:
            return f"10{num}"
    return None


# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================
def mostrar_dashboard():
    print("\n" + "=" * 55)
    print("           DASHBOARD DE PORTÁTILES Y PRÉSTAMOS")
    print("=" * 55)
    print(f"{'ID Equipo':<10} | {'Modelo':<22} | {'Estado':<20}")
    print("-" * 55)
    for id_eq, datos in equipos.items():
        print(f"{id_eq:<10} | {datos['modelo']:<22} | {datos['estado']:<20}")

    activos = [p for p in prestamos if p["fecha_devolucion"] is None]
    print("\n" + "-" * 55)
    print(f"PRÉSTAMOS ACTIVOS: {len(activos)}")
    print("-" * 55)
    if not activos:
        print("  (No hay préstamos activos)")
    for p in activos:
        print(f"• ID Préstamo #{p['id']} | Portátil: {p['id_equipo']} | Usuario: {p['id_usuario']}")
        print(f"  Salida: {p['fecha_salida'].strftime('%Y-%m-%d %H:%M')} | Límite: {p['fecha_limite'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  Responsable: {p['id_responsable']} | Motivo: {p['motivo'] or 'N/A'}")
    print("=" * 55)


def registrar_prestamo():
    print("\n--- FASE 1: REGISTRO DE PRÉSTAMO ---")
    id_input = input("ID del usuario solicitante (ej: 101, 102 o 103 [sancionado]): ").strip()
    id_usuario = buscar_usuario(id_input)
    if not id_usuario:
        print(f"❌ Error: El usuario '{id_input}' no está registrado.")
        return

    usuario = usuarios[id_usuario]

    # Prueba 2: Validar si el usuario está sancionado o tiene préstamo activo
    if usuario["sancionado"]:
        print(f"❌ BLOQUEO: El usuario {usuario['nombre']} (ID: {id_usuario}) tiene sanciones activas por retrasos o faltas.")
        return

    prestamo_previo = next((p for p in prestamos if p["id_usuario"] == id_usuario and p["fecha_devolucion"] is None), None)
    if prestamo_previo:
        print(f"❌ Error: El usuario ya tiene el equipo {prestamo_previo['id_equipo']} en préstamo activo.")
        return

    # Verificación de disponibilidad de equipos
    disponibles = [id_eq for id_eq, d in equipos.items() if d["estado"] == "Disponible"]
    if not disponibles:
        print("❌ Situación crítica: No hay equipos portátiles disponibles en este momento.")
        return

    print(f"Equipos disponibles: {', '.join(disponibles)}")
    id_eq_input = input("ID del computador portátil a prestar (ej: 1, 2, 3): ").strip()
    id_equipo = buscar_equipo(id_eq_input)

    if not id_equipo:
        print(f"❌ Error: ID de equipo inexistente ('{id_eq_input}').")
        return
    if equipos[id_equipo]["estado"] != "Disponible":
        print(f"❌ Error: El equipo {id_equipo} está en estado '{equipos[id_equipo]['estado']}'.")
        return

    id_responsable = input("ID numérico del responsable (ej: 901): ").strip() or "901"
    motivo = input("Motivo del préstamo (opcional): ").strip()
    horas_prestamo = input("Horas de préstamo permitidas (por defecto 4): ").strip()
    horas = int(horas_prestamo) if horas_prestamo.isdigit() else 4

    # Registro y asignación de tiempos
    ahora = datetime.now()
    limite = ahora + timedelta(hours=horas)

    nuevo_prestamo = {
        "id": len(prestamos) + 1,
        "id_usuario": id_usuario,
        "id_equipo": id_equipo,
        "id_responsable": id_responsable,
        "motivo": motivo,
        "fecha_salida": ahora,
        "fecha_limite": limite,
        "fecha_devolucion": None,
        "condicion_entrega": "Operativo / Buen estado",
        "condicion_devolucion": None,
    }

    prestamos.append(nuevo_prestamo)
    equipos[id_equipo]["estado"] = "Prestado"
    print(f"\n✅ Préstamo #{nuevo_prestamo['id']} registrado con éxito.")
    print(f"   Equipo {id_equipo} asignado a {usuario['nombre']} (ID: {id_usuario}). Devolución límite: {limite.strftime('%Y-%m-%d %H:%M')}")


def registrar_devolucion():
    print("\n--- FASE 2: REGISTRO DE DEVOLUCIÓN ---")
    id_eq_input = input("ID del computador que se devuelve (ej: 1, 2, 3): ").strip()
    id_equipo = buscar_equipo(id_eq_input)

    if not id_equipo:
        print(f"❌ Error: ID de equipo inexistente ('{id_eq_input}').")
        return

    prestamo_activo = next(
        (p for p in prestamos if p["id_equipo"] == id_equipo and p["fecha_devolucion"] is None),
        None
    )

    if not prestamo_activo:
        print(f"❌ Error: No se encontró ningún préstamo activo para el equipo {id_equipo}.")
        return

    ahora = datetime.now()
    prestamo_activo["fecha_devolucion"] = ahora

    # Verificación de retraso y aplicación de sanción
    if ahora > prestamo_activo["fecha_limite"]:
        print(f"⚠️ ALERTA: La devolución superó el tiempo límite ({prestamo_activo['fecha_limite'].strftime('%Y-%m-%d %H:%M')}).")
        usuarios[prestamo_activo["id_usuario"]]["sancionado"] = True
        print(f"   El usuario {prestamo_activo['id_usuario']} ha sido sancionado.")

    # Prueba 1: Inspección de daños físicos
    dano = input("¿El equipo presenta daños físicos o fallas? (s/n): ").strip().lower()
    if dano == "s":
        detalle = input("Describa el daño presentado: ").strip()
        prestamo_activo["condicion_devolucion"] = f"Dañado: {detalle}"
        equipos[id_equipo]["estado"] = "En revisión técnica"
        print(f"⚠️ Equipo {id_equipo} enviado a 'En revisión técnica'. Queda bloqueado para nuevos préstamos.")
    else:
        prestamo_activo["condicion_devolucion"] = "Buen estado"
        equipos[id_equipo]["estado"] = "Disponible"
        print(f"✅ Devolución completada. Equipo {id_equipo} vuelve a estar 'Disponible'.")


# ==============================================================================
# UTILIDADES DE CONSOLA Y NAVEGACIÓN
# ==============================================================================
def limpiar_pantalla():
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensaje="\nPresione Enter para volver al menú principal..."):
    """Pausa la ejecución para que el usuario pueda revisar la información antes de limpiar la pantalla."""
    try:
        import msvcrt
        if sys.stdin.isatty():
            print(mensaje, end="", flush=True)
            while True:
                ch = msvcrt.getch()
                if ch in (b'\r', b'\n', b'\x1b', b' '):
                    print()
                    return
                elif ch in (b'\x00', b'\xe0'):
                    msvcrt.getch()
    except Exception:
        pass

    try:
        input(mensaje)
    except (EOFError, KeyboardInterrupt):
        print()


def leer_opcion_menu(prompt=""):
    """
    Lee la opción seleccionada por el usuario en el menú principal.
    Permite salir inmediatamente presionando la tecla física Escape (ESC),
    o escribiendo 0, esc, escape, 1, 2, 3, etc.
    """
    # 1. Captura interactiva directa en Windows (msvcrt)
    try:
        import msvcrt
        if sys.stdin.isatty():
            print(prompt, end="", flush=True)
            buffer = []
            while True:
                char = msvcrt.getch()
                # Tecla física ESC (ASCII 27 / 0x1b) -> Salida inmediata
                if char == b'\x1b':
                    print("Esc")
                    return "0"
                # Tecla Enter
                elif char in (b'\r', b'\n'):
                    print()
                    return "".join(buffer).strip()
                # Tecla Backspace / Borrar
                elif char in (b'\x08', b'\x7f'):
                    if buffer:
                        buffer.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                # Teclas especiales (flechas, funciones)
                elif char in (b'\x00', b'\xe0'):
                    msvcrt.getch()
                # Caracteres normales imprimibles
                else:
                    try:
                        c = char.decode("utf-8", errors="ignore")
                        if c and c.isprintable():
                            buffer.append(c)
                            sys.stdout.write(c)
                            sys.stdout.flush()
                    except Exception:
                        pass
    except Exception:
        pass

    # 2. Captura interactiva directa en Unix / Linux / macOS (termios)
    try:
        import termios
        import tty
        import select
        if sys.stdin.isatty():
            print(prompt, end="", flush=True)
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            buffer = []
            try:
                tty.setcbreak(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch == '\x1b':  # Tecla ESC
                        r, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if r:
                            sys.stdin.read(2)
                            continue
                        print("Esc")
                        return "0"
                    elif ch in ('\r', '\n'):
                        print()
                        return "".join(buffer).strip()
                    elif ch in ('\x08', '\x7f'):
                        if buffer:
                            buffer.pop()
                            sys.stdout.write("\b \b")
                            sys.stdout.flush()
                    elif ch.isprintable():
                        buffer.append(ch)
                        sys.stdout.write(ch)
                        sys.stdout.flush()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception:
        pass

    # 3. Fallback estándar universal con input()
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


# ==============================================================================
# MENÚ PRINCIPAL
# ==============================================================================
def main():
    while True:
        limpiar_pantalla()
        print("=" * 45)
        print("  SISTEMA DE GESTIÓN DE PORTÁTILES (CONSOLA)")
        print("=" * 45)
        print("1. Ver Dashboard (Equipos y préstamos)")
        print("2. Registrar Préstamo (Fase 1)")
        print("3. Registrar Devolución (Fase 2)")
        print("0. Salir (o presione tecla Escape)")

        opcion = leer_opcion_menu("\nSeleccione una opción (1-3, 0 o Esc para salir): ").strip().upper()

        if opcion == "1":
            limpiar_pantalla()
            mostrar_dashboard()
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            registrar_prestamo()
            pausar()
        elif opcion == "3":
            limpiar_pantalla()
            registrar_devolucion()
            pausar()
        elif opcion in ("0", "ESC", "ESCAPE"):
            limpiar_pantalla()
            print("👋 Saliendo del sistema...\n")
            break
        else:
            print("\n❌ Opción inválida. Intente de nuevo.")
            pausar("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
