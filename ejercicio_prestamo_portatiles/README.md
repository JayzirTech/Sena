# 💻 Sistema de Préstamo de Computadores Portátiles

> **JayzirTech** — Solución interactiva por consola (TUI) para la gestión, seguimiento y control de inventario de portátiles en centros de formación u organizaciones.

---

## 📋 Descripción del Proyecto

El sistema automatiza el registro manual de préstamos de computadores, solucionando los problemas de saturación operativa, búsquedas lentas y errores de registro que ocurren al escalar el número de equipos en préstamo.

La aplicación está construida en **Python puro (sin dependencias externas)** con almacenamiento en memoria, ofreciendo una experiencia de terminal limpia y profesional.

---

## ✨ Características Principales

* 📊 **Dashboard en tiempo real:** Visualización instantánea del estado de todos los equipos y detalle de los préstamos activos con fechas límite y responsables.
* 📝 **Fase 1 (Registro de Préstamo):**
  * Verificación inmediata de disponibilidad de portátiles.
  * **Control de acceso:** Bloqueo automático de usuarios con sanciones disciplinarias activas.
  * **Regla de unicidad:** Bloqueo a usuarios que ya cuenten con un préstamo activo.
* 🔄 **Fase 2 (Registro de Devolución):**
  * Control de tiempos límite con aplicación automática de sanción en caso de retraso.
  * **Inspección de daños físicos:** Si el equipo presenta fallas o golpes, se envía automáticamente al estado `En revisión técnica` para evitar que vuelva a ser prestado.
* 🖥️ **Interfaz Ergonómica (TUI):**
  * **Limpieza de consola (`cls` / `clear`):** La pantalla se limpia por cada opción seleccionada para evitar acumulación de texto.
  * **Pausa contextual:** Permite leer con calma los reportes y confirmaciones antes de refrescar el menú principal.
  * **Salida rápida:** Soporte para salir digitando `0` o pulsando directamente la tecla física **`Escape` (ESC)**.
* 🔢 **Códigos 100% Numéricos:** Códigos simples y rápidos de digitar, optimizados para demostraciones en vivo.

---

## 🏷️ Catálogo de Códigos Numéricos

### Computadores Portátiles (Equipos)
| ID Equipo | Modelo | Estado Inicial |
| :---: | :--- | :--- |
| **`1`** | Dell Latitude 5420 | `Disponible` |
| **`2`** | Lenovo ThinkPad E14 | `Disponible` |
| **`3`** | HP ProBook 450 | `Disponible` |
| **`4`** | MacBook Air M1 | `En revisión técnica` *(Bloqueado)* |

> *Nota: El sistema acepta dígitos directos (`1`, `2`), formatos con ceros (`01`) o el formato clásico (`PORT-01`).*

### Usuarios Registrados
| ID Usuario | Atajo | Nombre | Estado Disciplinario |
| :---: | :---: | :--- | :--- |
| **`101`** | `1` | Carlos Gómez | ✅ Habilitado |
| **`102`** | `2` | Ana Rodríguez | ✅ Habilitada |
| **`103`** | `3` | Pedro Morales | ❌ **Sancionado** *(Caso de prueba)* |

> *Nota: Para agilizar las pruebas, puedes escribir tanto el ID completo `101` como su atajo directo `1`.*

### Responsable
* ID sugerido por defecto: **`901`** (basta con pulsar *Enter* para aceptarlo).

---

## 🚀 Requisitos y Ejecución

### Requisitos
* Python 3.7 o superior instalado.
* Compatible con **Windows**, **Linux** y **macOS** (utiliza exclusivamente librerías estándar como `os`, `sys`, `datetime` y `msvcrt` / `termios`).

### Instrucciones de Ejecución
Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
python sistema_prestamo_portatiles.py
```

---

## 🧪 Casos de Prueba para Demostración

### Caso 1: Bloqueo por Sanción Disciplinaria Activa
1. En el menú principal, selecciona la opción **`2`** *(Registrar Préstamo)*.
2. En ID del usuario solicitante, ingresa **`103`** (o solo **`3`**).
3. **Resultado:** El sistema detecta el historial de Pedro Morales y bloquea la operación emitiendo la alerta:
   `❌ BLOQUEO: El usuario Pedro Morales (ID: 103) tiene sanciones activas por retrasos o faltas.`

---

### Caso 2: Préstamo Exitoso y Seguimiento en Dashboard
1. Selecciona la opción **`2`** *(Registrar Préstamo)*.
2. Ingresa los datos:
   * **Usuario:** `101` (o `1`)
   * **Portátil:** `1`
   * **Responsable:** `901` (o pulsa Enter)
   * **Motivo:** `Taller de Sistemas`
   * **Horas:** `4`
3. Observa la confirmación del préstamo con hora de devolución calculada.
4. Pulsa Enter para volver al menú y selecciona **`1`** *(Ver Dashboard)*.
5. **Resultado:** El portátil `1` figura como `Prestado` y aparece detallado en la lista de préstamos activos.

---

### Caso 3: Devolución con Daño Físico
1. Selecciona la opción **`3`** *(Registrar Devolución)*.
2. Ingresa el equipo a devolver: **`1`**.
3. A la pregunta `¿El equipo presenta daños físicos o fallas? (s/n)`, responde **`s`**.
4. Escribe la descripción: `Bisagra dañada y pantalla con líneas`.
5. **Resultado:** El equipo pasa automáticamente al estado `En revisión técnica`, quedando bloqueado para futuros préstamos hasta su reparación.
6. Consulta el Dashboard (**`1`**) para verificar el nuevo estado.

---

### Caso 4: Salida Rápida
* En el menú principal, pulsa una sola vez la tecla física **`Escape` (ESC)** o escribe **`0`**. El sistema limpia la consola y se despide de forma limpia.

---

## 📁 Estructura del Repositorio

```text
ejercicio_prestamo_portatiles/
├── sistema_prestamo_portatiles.py   # Código fuente principal de la aplicación
├── taller_prestamo_portatiles.docx  # Documento base con los requerimientos y casos del taller
└── README.md                        # Documentación técnica y guía de presentación
```

