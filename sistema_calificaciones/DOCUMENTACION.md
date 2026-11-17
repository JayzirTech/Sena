# Manual de Usuario: Sistema de Calificaciones del Salón
**Guía de Uso para Docentes, Coordinadores y Aprendices**

> 📌 **Enlace Oficial del Repositorio:**  
> [https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones](https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones)

---

## 1. ¿Qué es este sistema?

Este sistema es una herramienta diseñada para facilitar la labor de los profesores y coordinadores en el registro de notas de un salón de clases. 

Permite llevar el control completo de los estudiantes, calcular sus promedios de manera automática y saber al instante si un estudiante aprueba o reprueba el año escolar, sin necesidad de hacer cuentas a mano ni usar complicadas hojas de cálculo.

---

## 2. ¿Cómo funciona el año escolar?

Para que todo sea justo y transparente, el sistema funciona con las siguientes reglas claras:

1. **Las 5 Materias del Salón:**
   Todos los aprendices ven exactamente 5 asignaturas:
   * Matemáticas
   * Literatura
   * Ciencias Sociales
   * Química
   * Programación de Software

2. **Los 4 Periodos Académicos:**
   * El año escolar está compuesto por 4 periodos (Periodo 1, 2, 3 y 4).
   * Los periodos siempre están disponibles para ingresar o corregir notas cuando el profesor lo necesite.

3. **¿Cómo se calcula la nota definitiva de cada materia?**
   * En cada periodo se pueden ingresar todas las notas que el docente desee. El sistema saca el promedio de ese periodo.
   * La nota final de la materia se calcula sumando el promedio de los 4 periodos y dividiendo siempre entre 4. Si un periodo aún no tiene notas, cuenta como cero hasta que se ingresen.

4. **¿Cómo se aprueba el año escolar?**
   * El estudiante aprueba el año si el promedio general de todas sus materias es **igual o superior a 70 puntos**.
   * La aprobación depende exclusivamente de este promedio general.

5. **Recuperaciones y Nivelaciones:**
   * Si un estudiante pierde una evaluación y presenta una recuperación, esa nueva nota se ingresa como una calificación adicional para ayudarle a subir su promedio en ese periodo.

---

## 3. Guía Paso a Paso: ¿Cómo usar el sistema?

### Regla de oro de navegación:
> 💡 **Para salir o volver atrás en cualquier menú o pantalla, simplemente presione el número `0`.**

---

### Paso 1: Registrar un nuevo aprendiz
* En el menú principal, elija la opción **[1]**.
* El sistema solo le pedirá dos datos sencillos:
  1. El número de documento de identidad (Tarjeta de Identidad o Cédula).
  2. El nombre y apellido del estudiante.
* **Usted no tiene que inventar códigos ni correos:** El sistema le asigna automáticamente un código ordenado (como `EST-0001`, `EST-0002`) y le crea de inmediato su correo institucional (ejemplo: `ana.gomez@sena.edu.co`).
* Antes de guardar, el sistema le mostrará un resumen y le preguntará si confirma el registro. Al confirmar, verá en pantalla la ficha definitiva del aprendiz.

---

### Paso 2: ¿Qué pasa si un estudiante se retira?
* Si un estudiante ya no pertenece a la institución, elija la opción **[2] Eliminar estudiante**.
* **Tranquilidad para el docente:** La información del estudiante y las notas que ya tenía no se destruyen en el archivo histórico; simplemente el sistema lo oculta para que ya no aparezca en las listas activas ni en los reportes del día a día.

---

### Paso 3: Calificar a un estudiante
* En el menú principal, elija la opción **[3] Registrar calificación**.
* El sistema le mostrará la lista de estudiantes para que elija a quién va a calificar. Si son muchos, puede escribir parte de su nombre o su cédula para encontrarlo de inmediato.
* Luego elija la materia, el periodo (del 1 al 4) y digite la nota obtenida (entre 0 y 100).
* Siempre se le pedirá confirmación antes de guardar la nota.

---

### Paso 4: Corregir o borrar una nota si hubo una equivocación
* Si digitó una nota por error, elija la opción **[4] Modificar o Eliminar calificación**.
* Seleccione al estudiante para ver todas las notas que tiene registradas.
* Elija la nota equivocada y decida si desea cambiarle el valor o eliminarla por completo. El sistema siempre le pedirá confirmar antes de hacer el cambio.

---

### Paso 5: Consultar Reportes y Boletines
El sistema le ofrece dos grandes módulos de consulta:

* **Opción [5] - Boletín Individual del Estudiante:**
  Permite ver la hoja de calificaciones completa de un estudiante: sus notas periodo por periodo, su nota final en cada materia, su promedio del año, si pasó o perdió y cómo va comparado con el promedio del salón.
* **Opción [6] - Resumen del Salón y de las Materias:**
  Permite ver la lista completa de todo el grupo, el promedio general del salón, cuántos estudiantes van aprobando y quién es el estudiante con el mejor promedio de la clase.

---

## 4. Seguridad y Confirmaciones

Para evitar que se pierdan datos o se hagan cambios por accidente:
* **Siempre se pide confirmación:** Cualquier acción importante le preguntará `¿Desea confirmar la operación? (S/N)`.
* **Protección contra cierres accidentales:** Si presiona la opción de salir (`0`), el programa le preguntará si está seguro de cerrar la aplicación.
