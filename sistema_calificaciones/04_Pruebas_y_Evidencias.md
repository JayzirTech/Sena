# SERVICIO NACIONAL DE APRENDIZAJE - SENA
## CENTRO DE COMERCIO Y SERVICIOS
### PROGRAMA DE FORMACIÓN: ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)

---

# 04. INFORME DE PRUEBAS DE ESCRITORIO, CALIDAD Y CORRECCIÓN DE ERRORES
## Reto Principal: “Sistema de Registro y Procesamiento de Calificaciones”
**Actividad de Aprendizaje:** Algoritmia y Lógica de Programación  
**Equipo de Desarrollo (Trabajo en Parejas):** Jayzir Martínez & Julián Vanegas  
**Entorno Tecnológico:** Python 3.13 / Pseudocódigo PSeInt / Traza Manual  

---

## 1. Justificación y Metodología de las Pruebas de Escritorio

La **prueba de escritorio** es una técnica manual fundamental de la ingeniería de software y la algoritmia que consiste en simular paso a paso la ejecución de un algoritmo siguiendo rigurosamente el flujo de control, las asignaciones en memoria y los operadores lógicos. Su objetivo pedagógico y técnico es:
1. Verificar que el algoritmo responda correctamente a la lógica de negocio sin depender de una máquina.
2. Identificar inconsistencias en la inicialización o acumulación de variables (como acumuladores que no se reinician en cada ciclo).
3. Evaluar el comportamiento en los límites de decisión (valores de frontera).
4. Corregir fallos tempranos antes de la codificación y puesta en producción.

---

## 2. Escenario 1: Prueba de Escritorio Formal Paso a Paso (Grupo Estándar)

Se establece un grupo de prueba con $N = 3$ aprendices y $M = 3$ calificaciones por aprendiz.

### Datos de Entrada del Escenario:
1. **Aprendiz 1:** Doc: `101` | Nombre: `Carlos Gómez` | Notas: `80.0`, `75.0`, `85.0`
2. **Aprendiz 2:** Doc: `102` | Nombre: `Ana Rodríguez` | Notas: `60.0`, `65.0`, `70.0`
3. **Aprendiz 3:** Doc: `103` | Nombre: `Julián Vanegas` | Notas: `70.0`, `70.0`, `70.0`

### Tabla de Traza de Ejecución Paso a Paso:

| Paso | Línea Algoritmo | `i` | `j` | `nombre` | `nota` | `suma_indiv` | `prom_indiv` | `estado` | `cont_aprob` | `cont_no_aprob` | `acum_general` | `prom_general` | Observaciones / Acción |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | Inicio | - | - | - | - | - | - | - | 0 | 0 | 0.0 | - | Inicialización de contadores y acumulador |
| **1** | Entrada | - | - | - | - | - | - | - | 0 | 0 | 0.0 | - | $N \leftarrow 3$, $M \leftarrow 3$ |
| **2** | Para `i=1` | 1 | - | "Carlos Gómez" | - | 0.0 | - | - | 0 | 0 | 0.0 | - | Reinicio de `suma_indiv` |
| **3** | Para `j=1` | 1 | 1 | "Carlos Gómez" | 80.0 | 80.0 | - | - | 0 | 0 | 0.0 | - | Suma nota 1 |
| **4** | Para `j=2` | 1 | 2 | "Carlos Gómez" | 75.0 | 155.0 | - | - | 0 | 0 | 0.0 | - | Suma nota 2 |
| **5** | Para `j=3` | 1 | 3 | "Carlos Gómez" | 85.0 | 240.0 | - | - | 0 | 0 | 0.0 | - | Suma nota 3 |
| **6** | Cálculo | 1 | - | "Carlos Gómez" | - | 240.0 | **80.00** | - | 0 | 0 | 0.0 | - | $240.0 / 3 = 80.00$ |
| **7** | Decisión | 1 | - | "Carlos Gómez" | - | 240.0 | 80.00 | **"Aprobado"** | **1** | 0 | 0.0 | - | $80.0 \ge 70.0$ (Verdadero) |
| **8** | Acumulación | 1 | - | "Carlos Gómez" | - | 240.0 | 80.00 | "Aprobado" | 1 | 0 | **80.00** | - | Acumula al grupo |
| **9** | Para `i=2` | 2 | - | "Ana Rodríguez" | - | 0.0 | - | - | 1 | 0 | 80.00 | - | Reinicio de `suma_indiv` para Aprendiz 2 |
| **10** | Para `j=1` | 2 | 1 | "Ana Rodríguez" | 60.0 | 60.0 | - | - | 1 | 0 | 80.00 | - | Suma nota 1 |
| **11** | Para `j=2` | 2 | 2 | "Ana Rodríguez" | 65.0 | 125.0 | - | - | 1 | 0 | 80.00 | - | Suma nota 2 |
| **12** | Para `j=3` | 2 | 3 | "Ana Rodríguez" | 70.0 | 195.0 | - | - | 1 | 0 | 80.00 | - | Suma nota 3 |
| **13** | Cálculo | 2 | - | "Ana Rodríguez" | - | 195.0 | **65.00** | - | 1 | 0 | 80.00 | - | $195.0 / 3 = 65.00$ |
| **14** | Decisión | 2 | - | "Ana Rodríguez" | - | 195.0 | 65.00 | **"No Aprobado"** | 1 | **1** | 80.00 | - | $65.0 < 70.0$ (Falso) |
| **15** | Acumulación | 2 | - | "Ana Rodríguez" | - | 195.0 | 65.00 | "No Aprobado" | 1 | 1 | **145.00** | - | $80.00 + 65.00 = 145.00$ |
| **16** | Para `i=3` | 3 | - | "Julián Vanegas" | - | 0.0 | - | - | 1 | 1 | 145.00 | - | Reinicio de `suma_indiv` para Aprendiz 3 |
| **17** | Para `j=1` | 3 | 1 | "Julián Vanegas" | 70.0 | 70.0 | - | - | 1 | 1 | 145.00 | - | Suma nota 1 |
| **18** | Para `j=2` | 3 | 2 | "Julián Vanegas" | 70.0 | 140.0 | - | - | 1 | 1 | 145.00 | - | Suma nota 2 |
| **19** | Para `j=3` | 3 | 3 | "Julián Vanegas" | 70.0 | 210.0 | - | - | 1 | 1 | 145.00 | - | Suma nota 3 |
| **20** | Cálculo | 3 | - | "Julián Vanegas" | - | 210.0 | **70.00** | - | 1 | 1 | 145.00 | - | $210.0 / 3 = 70.00$ |
| **21** | Decisión | 3 | - | "Julián Vanegas" | - | 210.0 | 70.00 | **"Aprobado"** | **2** | 1 | 145.00 | - | $70.0 \ge 70.0$ (Verdadero en frontera) |
| **22** | Acumulación | 3 | - | "Julián Vanegas" | - | 210.0 | 70.00 | "Aprobado" | 2 | 1 | **215.00** | - | $145.00 + 70.00 = 215.00$ |
| **23** | Fin Ciclo `i` | - | - | - | - | - | - | - | 2 | 1 | 215.00 | - | Salida del bucle principal |
| **24** | Prom. Grupo | - | - | - | - | - | - | - | 2 | 1 | 215.00 | **71.67** | $215.00 / 3 = 71.67$ |
| **25** | Reporte | - | - | - | - | - | - | - | 2 (66.7%) | 1 (33.3%) | 215.00 | 71.67 | Impresión de consolidados finales |

---

## 3. Escenarios Adicionales de Prueba

### 3.1 Escenario 2: Prueba de Frontera y Límite de Aprobación
* **Objetivo:** Verificar que el sistema respete estrictamente la condición de aprobación institucional ($\ge 70.0$).
* **Casos Evaluados:**
  * Aprendiz A: Notas $[69.0, 70.0, 70.0] \rightarrow \text{Promedio} = 69.67$. Resultado: **"No Aprobado"** (Correcto).
  * Aprendiz B: Notas $[70.0, 70.0, 70.0] \rightarrow \text{Promedio} = 70.00$. Resultado: **"Aprobado"** (Correcto, valida operador $\ge$).
  * Aprendiz C: Notas $[70.0, 71.0, 70.0] \rightarrow \text{Promedio} = 70.33$. Resultado: **"Aprobado"** (Correcto).

### 3.2 Escenario 3: Valores Extremos (Mínimo y Máximo)
* **Objetivo:** Evaluar la estabilidad del algoritmo ante el techo y el piso de la escala numérica.
* **Casos Evaluados:**
  * Aprendiz Excelencia: Notas $[100.0, 100.0, 100.0, 100.0] \rightarrow \text{Promedio} = 100.00$. Estado: **"Aprobado"**.
  * Aprendiz Nulo: Notas $[0.0, 0.0, 0.0, 0.0] \rightarrow \text{Promedio} = 0.00$. Estado: **"No Aprobado"**.
* **Resultado:** El acumulador no sufre desbordamientos ni errores de precisión de coma flotante.

### 3.3 Escenario 4: Pruebas de Robustez y Manejo de Errores de Entrada
* **Objetivo:** Verificar que el sistema no colapse ante ingresos no válidos por parte del usuario.

| Entrada Ingresada | Tipo de Error | Comportamiento del Algoritmo | Estado de Corrección |
| :--- | :--- | :--- | :---: |
| Cantidad de aprendices = `0` | División por cero en promedio | Bucle `Repetir...Hasta Que` exige $N \ge 1$ | Corregido |
| Calificación = `125.0` | Valor fuera de escala superior | Validación rechaza y solicita reingreso ($0.0 - 100.0$) | Corregido |
| Calificación = `-15.0` | Valor negativo inválido | Validación rechaza y solicita reingreso | Corregido |
| Calificación = `"ochenta"` | Error de tipo de dato (ValueError) | Bloque `try-except` captura excepción y repite solicitud | Corregido |
| Documento o Nombre vacío | Cadena vacía o puros espacios | Función `leer_texto_no_vacio()` exige texto real | Corregido |
| Calificación con coma (`85,5`) | Conflicto regional de decimal | Conversión `.replace(',', '.')` estandariza a flotante | Corregido |

---

## 4. Bitácora de Errores Encontrados y Correcciones Realizadas

Durante el ciclo de desarrollo en parejas se registraron 4 discrepancias que fueron documentadas y solventadas:

### Error 1: Acumulador individual no reiniciado dentro del ciclo principal
* **Descripción del Fallo:** En el borrador inicial del pseudocódigo, la instrucción `suma_indiv <- 0` se encontraba colocada antes del ciclo `Para i <- 1 Hasta N`. Como consecuencia, las notas del segundo aprendiz se sumaban a las del primero, produciendo promedios superiores a 100 e incorrectos.
* **Causa Raíz:** Falta de ámbito local para el acumulador individual.
* **Corrección Aplicada:** Se reubicó la asignación `suma_indiv <- 0.0` inmediatamente después del inicio del ciclo de cada aprendiz (`Para i`).

### Error 2: Uso del operador relacional mayor estricto (`>`) en vez de mayor o igual (`>=`)
* **Descripción del Fallo:** Al ejecutar la prueba con un aprendiz con promedio exacto de $70.0$, el sistema lo catalogaba como "No Aprobado".
* **Causa Raíz:** La instrucción condicional original leía: `Si promedio > 70 Entonces`.
* **Corrección Aplicada:** Se corrigió el operador relacional a `Si promedio >= UMBRAL_APROBACION Entonces` para cumplir textualmente la condición institucional de aprobación.

### Error 3: Riesgo de división por cero al calcular el promedio general
* **Descripción del Fallo:** Si en la ejecución se permitía ingresar $0$ en la cantidad de aprendices, el programa arrojaba un error de terminación abrupta (`ZeroDivisionError`).
* **Causa Raíz:** Ausencia de validación previa en la cantidad de registros.
* **Corrección Aplicada:** Se agregó la función de validación `leer_entero_positivo(minimo=1)` y el bucle defensivo en pseudocódigo `Hasta Que num_aprendices > 0`.

### Error 4: Discrepancia en el separador decimal (coma vs punto)
* **Descripción del Fallo:** Al ingresar notas como `75,5` en teclados latinoamericanos, Python generaba una excepción `ValueError`.
* **Causa Raíz:** En Python los números reales se definen con punto decimal (`.`), mientras que en español es común la coma (`,`).
* **Corrección Aplicada:** Se implementó una normalización automática mediante `.strip().replace(',', '.')` antes de parsear a `float`.

---

## 5. Guía de Sustentación Oral y Defensa ante el Instructor

Para la sustentación individual o en parejas ante la instructora o evaluador, se recomiendan los siguientes argumentos técnicos:

1. **Sobre la Estructura de Arreglos:**
   > *"Elegimos utilizar una matriz bidimensional `matriz[i][j]` y vectores paralelos porque esto nos permite mantener la trazabilidad completa en memoria. Si quisiéramos ordenar los aprendices por su promedio o exportar las actas en diferentes momentos, no tenemos que pedirle al usuario que vuelva a ingresar las notas."*

2. **Sobre la Lógica de Decisión:**
   > *"La estructura de decisión utilizada es un condicional doble `Si...Entonces...Sino`. El punto crítico verificado en la prueba de escritorio fue el valor en frontera $70.0$. Usar `>=` en lugar de `>` garantiza que ningún aprendiz sea perjudicado injustamente cuando alcanza la nota mínima aprobatoria."*

3. **Sobre el Cálculo del Promedio Grupal:**
   > *"El promedio del grupo se calcula mediante un acumulador general `acum_general` que suma los promedios individuales al término de cada ciclo de aprendiz. Al finalizar, se divide entre el total de aprendices $N$. Garantizamos matemáticamente que nunca habrá división por cero porque la entrada $N$ está blindada con una validación que exige un mínimo de 1 aprendiz."*

4. **Sobre la Robustez y Calidad del Software:**
   > *"Todo el código fue blindado con bloques de captura de excepciones (`try-except`) y validadores de rangos. Si un usuario digita texto donde van números o introduce una nota como 150, el sistema le explica el error y le solicita de nuevo el dato sin cerrarse repentinamente."*
