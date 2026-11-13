# SERVICIO NACIONAL DE APRENDIZAJE - SENA
## CENTRO DE COMERCIO Y SERVICIOS
### PROGRAMA DE FORMACIÓN: ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)

---

# 01. DOCUMENTO DE ANÁLISIS Y DISEÑO LÓGICO
## Reto Principal: “Sistema de Registro y Procesamiento de Calificaciones”
**Actividad de Aprendizaje:** Algoritmia y Lógica de Programación  
**Equipo de Desarrollo (Trabajo en Parejas):** Jayzir Martínez & Julián Vanegas  
**Entorno Tecnológico:** Algoritmia Estructurada (Pseudocódigo PSeInt / Estándar SENA) & Python 3.13  

---

## 1. Lectura y Comprensión de la Situación Problema

### 1.1 Contexto y Necesidad
Una institución educativa de formación para el trabajo requiere automatizar y estandarizar el proceso manual de gestión evaluativa. Actualmente, los instructores consolidan de forma manual las calificaciones obtenidas por los aprendices a lo largo de las distintas evidencias de aprendizaje. Este procedimiento manual acarrea riesgos de error humano en el cálculo de promedios, discrepancias al determinar la aprobación de los aprendices y lentitud en la generación de consolidados estadísticos para la coordinación académica.

Para resolver esta problemática, se solicita el diseño y desarrollo de un algoritmo robusto, ordenado y escalable que cumpla con los siguientes requerimientos fundamentales:
1. Registrar de manera estructurada las calificaciones de múltiples aprendices pertenecientes a un grupo formativo.
2. Calcular el promedio aritmético ponderado/individual obtenido por cada aprendiz en sus respectivas evaluaciones.
3. Determinar de forma automática y unificada el estado académico final de cada aprendiz (**"Aprobado"** o **"No Aprobado"**), tomando como criterio de decisión institucional una calificación promedio **mayor o igual a 70 puntos (sobre 100)**.
4. Consolidar al finalizar el procesamiento de todos los registros el **promedio general del grupo**, así como indicadores estadísticos clave de rendimiento colectivo (total evaluados, tasa porcentual de aprobación, calificación más alta y más baja).
5. Respaldar la información procesada en un formato legible para fines de auditoría académica y seguimiento formativo.

### 1.2 Reglas de Negocio Institucionales
* **Escala de Calificación:** Las notas individuales se expresan en escala cuantitativa continua de **0.0 a 100.0**.
* **Condición Estricta de Aprobación:** 
  $$\text{Estado} = \begin{cases} \text{"Aprobado"} & \text{si } \text{Promedio} \ge 70.0 \\ \text{"No Aprobado"} & \text{si } \text{Promedio} < 70.0 \end{cases}$$
* **Escalabilidad del Grupo:** El algoritmo debe ser dinámico, permitiendo procesar cualquier cantidad $N \ge 1$ de aprendices y cualquier número $M \ge 1$ de notas por aprendiz.

---

## 2. Descomposición del Problema (Matriz E-P-S)

Para abordar la solución de manera metódica, descomponemos el problema en sus tres componentes cardinales: **Entradas**, **Procesos** y **Salidas**.

| ENTRADAS (Datos requeridos) | PROCESOS (Algoritmos, validaciones y transformaciones) | SALIDAS (Resultados esperados) |
| :--- | :--- | :--- |
| • Cantidad de aprendices del grupo ($N$).<br>• Cantidad de notas por aprendiz ($M$).<br>• Por cada aprendiz:<br>&nbsp;&nbsp;- Documento de identificación o Ficha.<br>&nbsp;&nbsp;- Nombres y apellidos completos.<br>&nbsp;&nbsp;- Calificaciones individuales ($\text{nota}_{1}, \text{nota}_{2}, \dots, \text{nota}_{M}$). | 1. **Validación de rangos:** Asegurar $N > 0$, $M > 0$ y $0.0 \le \text{nota} \le 100.0$.<br>2. **Ciclo exterior (por aprendiz):** Itera desde $1$ hasta $N$.<br>3. **Ciclo interior (por nota):** Itera desde $1$ hasta $M$, acumulando: $\text{suma\_notas} \leftarrow \text{suma\_notas} + \text{nota}_j$.<br>4. **Cálculo de promedio individual:** $\text{promedio}_i \leftarrow \frac{\text{suma\_notas}}{M}$.<br>5. **Estructura de decisión lógica:** Evaluar si $\text{promedio}_i \ge 70.0$ para asignar estado.<br>6. **Acumulación grupal:** $\text{acum\_general} \leftarrow \text{acum\_general} + \text{promedio}_i$.<br>7. **Conteo estadístico:** Incrementar contadores de aprobados o no aprobados.<br>8. **Cálculo de promedio del grupo:** $\text{promedio\_general} \leftarrow \frac{\text{acum\_general}}{N}$.<br>9. **Identificación de extremos:** Determinar mayor y menor promedio del grupo. | • **Boletín individual por pantalla:**<br>&nbsp;&nbsp;- Documento y Nombre del aprendiz.<br>&nbsp;&nbsp;- Vector de notas obtenidas.<br>&nbsp;&nbsp;- Promedio individual con 2 decimales.<br>&nbsp;&nbsp;- Veredicto: "Aprobado" o "No Aprobado".<br><br>• **Informe consolidado del grupo:**<br>&nbsp;&nbsp;- Total de aprendices evaluados.<br>&nbsp;&nbsp;- **Promedio general del grupo**.<br>&nbsp;&nbsp;- Conteo y porcentaje de aprobación.<br>&nbsp;&nbsp;- Conteo y porcentaje de reprobación.<br>&nbsp;&nbsp;- Aprendiz con calificación más alta y más baja.<br><br>• **Persistencia en archivo plano:** `03_Registros_Calificaciones.txt`. |

---

## 3. Definición y Diccionario de Variables

Para evitar ambigüedades lógicas y garantizar la integridad de memoria del sistema, se formalizan las variables requeridas:

| Variable | Tipo de Dato | Ámbito | Rango / Formato | Propósito / Rol en el Algoritmo |
| :--- | :---: | :---: | :---: | :--- |
| `UMBRAL_APROBACION` | Real (Constante) | Global | $70.0$ | Constante que define el valor mínimo para aprobar. |
| `num_aprendices` ($N$) | Entero | Global / Principal | $1 \le N \le 1000$ | Almacena el número total de aprendices a evaluar. |
| `num_notas` ($M$) | Entero | Global / Principal | $1 \le M \le 20$ | Número de calificaciones asignadas por aprendiz. |
| `i` | Entero | Local (Bucle) | $1 \dots N$ | Variable de control para el ciclo de aprendices. |
| `j` | Entero | Local (Bucle) | $1 \dots M$ | Variable de control para el ciclo de notas individuales. |
| `id_doc` | Cadena (Texto) | Local | Alfanumérico | Documento de identidad del aprendiz en proceso. |
| `nombre` | Cadena (Texto) | Local | Alfabético | Nombres y apellidos completos del aprendiz. |
| `nota_actual` | Real | Local | $0.0 \dots 100.0$ | Calificación individual leída y validada en cada paso. |
| `suma_notas_indiv` | Real | Local | $0.0 \dots (100.0 \times M)$ | Acumulador de las notas de un solo aprendiz. |
| `promedio_indiv` | Real | Local | $0.0 \dots 100.0$ | Promedio aritmético individual obtenido. |
| `estado_aprendiz` | Cadena | Local | "Aprobado" / "No Aprobado" | Etiqueta resultante de la estructura de decisión. |
| `acum_promedios_grupo` | Real | Global | $\ge 0.0$ | Acumulador que totaliza la suma de todos los promedios. |
| `cont_aprobados` | Entero | Global | $0 \dots N$ | Contador de aprendices con promedio $\ge 70.0$. |
| `cont_no_aprobados` | Entero | Global | $0 \dots N$ | Contador de aprendices con promedio $< 70.0$. |
| `promedio_general` | Real | Global | $0.0 \dots 100.0$ | Promedio aritmético global del grupo de aprendices. |
| `pct_aprobados` | Real | Global | $0.0 \dots 100.0\%$ | Porcentaje de estudiantes que aprobaron la formación. |
| `mejor_promedio` | Real | Global | $0.0 \dots 100.0$ | Registro del valor de calificación promedio más alto. |
| `peor_promedio` | Real | Global | $0.0 \dots 100.0$ | Registro del valor de calificación promedio más bajo. |

---

## 4. Identificación y Justificación del Uso de Arreglos

### 4.1 ¿Qué información se almacena en arreglos?
El análisis técnico identifica la necesidad de estructurar los datos mediante las siguientes estructuras homogéneas e indexadas:

1. **Arreglo Unidimensional de Nombres y Documentos (`nombres[]`, `documentos[]`):**
   - Vectores de cadenas que almacenan los datos de identidad de los aprendices asociados por su índice cardinal $i$.
2. **Arreglo Bidimensional de Calificaciones (`matriz_calificaciones[][]`):**
   - Matriz de tamaño $N \times M$ donde la fila $i$ representa al aprendiz y la columna $j$ representa su calificación en la actividad evaluativa $j$.
3. **Arreglo Unidimensional de Promedios (`promedios[]`):**
   - Vector de números reales que guarda de manera permanente en memoria el promedio final calculado para cada aprendiz.
4. **Arreglo Unidimensional de Estados Académicos (`estados[]`):**
   - Vector alfanumérico o booleano que retiene el dictamen de aprobación ("Aprobado" / "No Aprobado").

```
                 ESTRUCTURA DE ARREGLOS EN MEMORIA
                 
  Índice (i)      Documento      Nombre               Matriz Notas (j=1..M)      Promedio    Estado
┌────────────┬──────────────┬────────────────────┬─────────────────────────────┬───────────┬─────────────┐
│     0      │    "1001"    │ "Carlos Gómez"     │ [ 85.0 , 90.0 , 88.0 , 92.0]│   88.75   │  Aprobado   │
│     1      │    "1002"    │ "Ana Rodríguez"    │ [ 60.0 , 65.0 , 70.0 , 68.0]│   65.75   │ No Aprobado │
│     2      │    "1003"    │ "Julián Vanegas"   │ [ 70.0 , 70.0 , 70.0 , 70.0]│   70.00   │  Aprobado   │
│     3      │    "1004"    │ "Jayzir Martínez"  │ [ 95.0 , 98.0 , 94.0 , 100 ]│   96.75   │  Aprobado   │
│     4      │    "1005"    │ "Laura Pérez"      │ [ 45.0 , 50.0 , 58.0 , 52.0]│   51.25   │ No Aprobado │
└────────────┴──────────────┴────────────────────┴─────────────────────────────┴───────────┴─────────────┘
```

### 4.2 Justificación Técnica y Pedagógica
* **Desacoplamiento entre Captura y Reportes:** Sin arreglos, las notas y promedios de aprendices anteriores se sobrescribirían al procesar al siguiente. El uso de arreglos permite almacenar la información durante toda la sesión.
* **Cálculo de Estadísticas Posteriores sin Redigitadas:** Al tener los promedios en un vector, se pueden calcular desviaciones, ordenar los aprendices por rendimiento (ranking), encontrar máximos/mínimos y emitir reportes tantas veces como sea necesario.
* **Persistencia Integral:** Facilita la exportación a archivos planos (`.txt`) recorriendo los índices en una única pasada estructurada.
* **Eficiencia Algorítmica:** El acceso a los datos de cualquier aprendiz se realiza en tiempo constante $O(1)$ a través de su posición o índice en el arreglo.

---

## 5. Diseño del Algoritmo en Pseudocódigo

El siguiente pseudocódigo sigue el estándar formal de la formación SENA (compatible con el intérprete pedagógico PSeInt):

```pseudocode
Algoritmo SistemaRegistroCalificaciones
    // Definición de variables escalares
    Definir num_aprendices, num_notas, i, j Como Entero
    Definir cont_aprobados, cont_no_aprobados Como Entero
    Definir nota_actual, suma_indiv, prom_indiv Como Real
    Definir acum_general, prom_general Como Real
    Definir mejor_prom, peor_prom Como Real
    Definir nombre_destacado, nombre_refuerzo Como Caracter
    
    // Constante de Aprobación
    Definir UMBRAL_APROBACION Como Real
    UMBRAL_APROBACION <- 70.0
    
    Escribir "=========================================================="
    Escribir "  SISTEMA DE REGISTRO Y PROCESAMIENTO DE CALIFICACIONES"
    Escribir "=========================================================="
    
    // Paso 1: Lectura y validación de dimensiones
    Repetir
        Escribir "Ingrese la cantidad de aprendices a procesar (N > 0):"
        Leer num_aprendices
    Hasta Que num_aprendices > 0
    
    Repetir
        Escribir "Ingrese la cantidad de notas por aprendiz (M > 0):"
        Leer num_notas
    Hasta Que num_notas > 0
    
    // Paso 2: Dimensionamiento de los arreglos
    Dimension documentos[num_aprendices]
    Dimension nombres[num_aprendices]
    Dimension matriz_calificaciones[num_aprendices, num_notas]
    Dimension promedios[num_aprendices]
    Dimension estados[num_aprendices]
    
    // Paso 3: Inicialización de acumuladores y contadores generales
    acum_general <- 0.0
    cont_aprobados <- 0
    cont_no_aprobados <- 0
    mejor_prom <- -1.0
    peor_prom <- 101.0
    
    // Paso 4: Ciclo principal para procesar a cada aprendiz
    Para i <- 1 Hasta num_aprendices Con Paso 1 Hacer
        Escribir "----------------------------------------------------------"
        Escribir "REGISTRO DE DATOS - APRENDIZ ", i, " DE ", num_aprendices
        Escribir "----------------------------------------------------------"
        
        Escribir "Ingrese Documento de Identidad:"
        Leer documentos[i]
        
        Escribir "Ingrese Nombres y Apellidos:"
        Leer nombres[i]
        
        // Inicializar acumulador individual
        suma_indiv <- 0.0
        
        // Ciclo anidado para capturar y validar las calificaciones
        Para j <- 1 Hasta num_notas Con Paso 1 Hacer
            Repetir
                Escribir "  Ingrese Calificación ", j, " (Entre 0.0 y 100.0):"
                Leer nota_actual
                Si nota_actual < 0.0 O nota_actual > 100.0 Entonces
                    Escribir "  [ERROR] Nota inválida. Debe estar en el rango de 0 a 100."
                FinSi
            Hasta Que nota_actual >= 0.0 Y nota_actual <= 100.0
            
            // Guardar en la matriz y acumular
            matriz_calificaciones[i, j] <- nota_actual
            suma_indiv <- suma_indiv + nota_actual
        FinPara
        
        // Cálculo del promedio individual
        prom_indiv <- suma_indiv / num_notas
        promedios[i] <- prom_indiv
        
        // Estructura de decisión lógica para determinar el estado (Acción 6)
        Si prom_indiv >= UMBRAL_APROBACION Entonces
            estados[i] <- "Aprobado"
            cont_aprobados <- cont_aprobados + 1
        Sino
            estados[i] <- "No Aprobado"
            cont_no_aprobados <- cont_no_aprobados + 1
        FinSi
        
        // Acumular para el promedio general del grupo
        acum_general <- acum_general + prom_indiv
        
        // Actualizar valores extremos (máximo y mínimo)
        Si prom_indiv > mejor_prom Entonces
            mejor_prom <- prom_indiv
            nombre_destacado <- nombres[i]
        FinSi
        
        Si prom_indiv < peor_prom Entonces
            peor_prom <- prom_indiv
            nombre_refuerzo <- nombres[i]
        FinSi
        
        Escribir "=> Promedio: ", prom_indiv, " | Estado: ", estados[i]
    FinPara
    
    // Paso 5: Cálculo del promedio general del grupo (Acción 7)
    prom_general <- acum_general / num_aprendices
    
    // Paso 6: Presentación de resultados y reportes
    Escribir ""
    Escribir "=========================================================="
    Escribir "          LISTADO FINAL DE CALIFICACIONES"
    Escribir "=========================================================="
    Escribir "DOC        | APRENDIZ                     | PROMEDIO | ESTADO"
    Escribir "----------------------------------------------------------"
    Para i <- 1 Hasta num_aprendices Con Paso 1 Hacer
        Escribir documentos[i], " | ", nombres[i], " | ", promedios[i], " | ", estados[i]
    FinPara
    Escribir "----------------------------------------------------------"
    
    // Paso 7: Presentación del resumen consolidado del grupo
    Escribir ""
    Escribir "=========================================================="
    Escribir "       RESUMEN CONSOLIDADO Y ESTADÍSTICAS DEL GRUPO"
    Escribir "=========================================================="
    Escribir "Total de aprendices evaluados: ", num_aprendices
    Escribir "Suma total acumulada de notas: ", acum_general
    Escribir "PROMEDIO GENERAL DEL GRUPO:   ", prom_general
    Escribir "Total de Aprobados (>= 70):    ", cont_aprobados, " (", (cont_aprobados / num_aprendices) * 100, "%)"
    Escribir "Total de No Aprobados (< 70): ", cont_no_aprobados, " (", (cont_no_aprobados / num_aprendices) * 100, "%)"
    Escribir "Mejor promedio obtenido:       ", mejor_prom, " (", nombre_destacado, ")"
    Escribir "Menor promedio obtenido:       ", peor_prom, " (", nombre_refuerzo, ")"
    Escribir "=========================================================="
    
    // Diagnóstico pedagógico institucional
    Si prom_general >= UMBRAL_APROBACION Entonces
        Escribir "DIAGNÓSTICO: El grupo superó satisfactoriamente el estándar formativo."
    Sino
        Escribir "DIAGNÓSTICO: El grupo requiere acciones de acompañamiento pedagógico."
    FinSi
FinAlgoritmo
```

---

## 6. Estructura de Decisión Lógica para el Estado de Aprobación

La lógica condicional para dictaminar si el aprendiz aprobó o no responde a una **estructura de decisión simple de doble vía (`Si...Entonces...Sino`)**:

$$\text{Decisión} = \begin{cases} 
\text{Verdadero} \longrightarrow \text{estado} \leftarrow \text{"Aprobado"}, \text{cont\_aprobados} \leftarrow \text{cont\_aprobados} + 1 & \text{si } \text{promedio} \ge 70.0 \\ 
\text{Falso} \longrightarrow \text{estado} \leftarrow \text{"No Aprobado"}, \text{cont\_no\_aprobados} \leftarrow \text{cont\_no\_aprobados} + 1 & \text{si } \text{promedio} < 70.0 
\end{cases}$$

### Análisis de la Condición en la Frontera (Análisis de Límite):
Un punto crítico detectado y resuelto en la etapa de diseño radica en la distinción entre el operador de comparación estricto (`>`) y el operador de inclusión mayor o igual (`>=`):
* Si un aprendiz obtiene exactamente **$70.00$**:
  * Con `promedio > 70.0` $\rightarrow$ Resultaría **Falso** (No Aprobado) $\Longrightarrow$ **¡Error de lógica!**
  * Con `promedio >= 70.0` $\rightarrow$ Resulta **Verdadero** (Aprobado) $\Longrightarrow$ **Comportamiento correcto según las especificaciones del reto**.
* Si un aprendiz obtiene **$69.99$**:
  * Con `promedio >= 70.0` $\rightarrow$ Resulta **Falso** (No Aprobado), respetando el umbral mínimo exigido.

---

## 7. Cálculo y Presentación del Promedio General del Grupo

El cálculo del promedio grupal se formaliza como la media aritmética de los promedios individuales:

$$\bar{X}_{\text{grupo}} = \frac{1}{N} \sum_{i=1}^{N} \text{promedio}_i = \frac{\text{acum\_general}}{N}$$

### Controles de Integridad y Robustez:
1. **Control de División por Cero:** El algoritmo valida previamente que $N \ge 1$ mediante un ciclo `Repetir...Hasta Que`, asegurando que el denominador jamás sea nulo.
2. **Conservación de Precisión Aritmética:** Las sumatorias y cocientes se almacenan en variables de punto flotante de doble precisión (tipo `Real` / `float`), redondeando únicamente al momento de la salida visual a dos dígitos decimales.
3. **Métricas Derivadas:** Se incorporan la tasa porcentual de éxito formativo:
   $$\% \text{ Aprobación} = \left( \frac{\text{cont\_aprobados}}{N} \right) \times 100$$
   y la tasa porcentual de no aprobación:
   $$\% \text{ No Aprobación} = \left( \frac{\text{cont\_no\_aprobados}}{N} \right) \times 100$$
