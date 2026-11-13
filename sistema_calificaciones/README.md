# 🎓 Sistema de Registro y Procesamiento de Calificaciones

> **Servicio Nacional de Aprendizaje (SENA) — Centro de Comercio y Servicios**  
> **Programa de Formación:** Análisis y Desarrollo de Software (ADSO)  
> **Actividad de Aprendizaje:** Algoritmia y Lógica de Programación  
> **Equipo de Desarrollo (Trabajo en Parejas):** Jayzir Martínez & Julián Vanegas  
> **Organización:** [JayzirTech](https://github.com/JayzirTech)

---

## 📌 Descripción de la Actividad

Una institución educativa necesita un algoritmo que permita registrar las calificaciones de varios aprendices, calcular el promedio de cada uno, determinar si aprobó o no y, al finalizar, mostrar el promedio general del grupo.

Este repositorio contiene la solución completa, técnica, documental y algorítmica desarrollada en estricto cumplimiento de las 8 acciones requeridas por el reto institucional.

---

## 🗂️ Estructura de Entregables en la Carpeta

Todos los recursos se encuentran centralizados dentro de la carpeta `sistema_calificaciones/`:

| Archivo | Formato | Descripción / Contenido |
| :--- | :---: | :--- |
| **[`01_Analisis_y_Diseno.docx`](./01_Analisis_y_Diseno.docx)** | DOCX | Documento formal con portada SENA, comprensión del problema, matriz E-P-S, diccionario de variables, justificación de arreglos, algoritmo en pseudocódigo y estructuras de decisión. |
| **[`01_Analisis_y_Diseno.md`](./01_Analisis_y_Diseno.md)** | Markdown | Versión en texto estructurado de la documentación de análisis y diseño lógico. |
| **[`02_Sistema_Calificaciones.py`](./02_Sistema_Calificaciones.py)** | Python | Programa interactivo en consola (TUI) con captura y validación robusta de notas, carga de casos de prueba, boletín individual, estadísticas consolidadas y exportación. |
| **[`03_Registros_Calificaciones.txt`](./03_Registros_Calificaciones.txt)** | TXT Plano | Archivo persistente estructurado con la matriz de aprendices, notas, promedios, estados y resumen del grupo. |
| **[`04_Pruebas_y_Evidencias.docx`](./04_Pruebas_y_Evidencias.docx)** | DOCX | Informe de calidad con la prueba de escritorio paso a paso, análisis en frontera (70.0), valores extremos, pruebas de robustez y bitácora de correcciones. |
| **[`04_Pruebas_y_Evidencias.md`](./04_Pruebas_y_Evidencias.md)** | Markdown | Versión en texto estructurado del informe de pruebas y aseguramiento de calidad. |
| **[`generar_documentos.py`](./generar_documentos.py)** | Python | Script automatizado para recompilar y generar los documentos `.docx` con tipografía, colores y tablas institucionales. |
| **[`README.md`](./README.md)** | Markdown | Guía general, técnica y operativa de la actividad formativa. |

---

## 📋 Cumplimiento de las 8 Acciones del Reto

| # | Acción Requerida | Implementación y Evidencia |
| :-: | :--- | :--- |
| **1** | **Leer y comprender la situación problema** | Desarrollado en la Sección 1 de `01_Analisis_y_Diseno.docx/.md`, detallando el contexto educativo, el alcance y las reglas de negocio. |
| **2** | **Descomponer el problema (Matriz E-P-S)** | Matriz formal de Entrada-Proceso-Salida documentada en la Sección 2 de `01_Analisis_y_Diseno.docx/.md`. |
| **3** | **Definir variables (notas, promedios, acumuladores)** | Diccionario técnico con 13 variables especificadas con tipo de dato, rango y ámbito en la Sección 3 de `01_Analisis_y_Diseno.docx/.md`. |
| **4** | **Identificar qué información puede almacenarse en un arreglo** | Justificación del uso de arreglos unidimensionales (`nombres`, `promedios`, `estados`) y arreglo bidimensional (`matriz_calificaciones[N][M]`) en la Sección 4. |
| **5** | **Diseñar algoritmo en pseudocódigo con ciclo** | Pseudocódigo estandarizado en sintaxis PSeInt / SENA implementado en la Sección 5 con ciclos `Para` anidados y bucles defensivos `Repetir...Hasta Que`. |
| **6** | **Incorporar estructura de decisión (Aprobación >= 70)** | Condicional doble `Si promedio >= 70.0 Entonces "Aprobado" Sino "No Aprobado"` con análisis de frontera documentado en la Sección 6. |
| **7** | **Calcular y presentar el promedio general del grupo** | Acumulación de promedios individuales y división entre el total de aprendices $N$, con porcentaje de aprobación, máxima y mínima nota. |
| **8** | **Pruebas de escritorio y corrección de errores** | Traza manual línea por línea de 25 pasos, 4 escenarios de prueba y bitácora de 4 errores solventados en `04_Pruebas_y_Evidencias.docx/.md`. |

---

## 💻 Instrucciones de Ejecución

### Requisitos
- **Python 3.8 o superior** (probado y validado en Python 3.13).
- No requiere dependencias externas para ejecutar el programa principal (`02_Sistema_Calificaciones.py`).

### Ejecutar el Programa Principal

Desde la consola o terminal en la raíz del repositorio o dentro de la carpeta:

```bash
# Ejecución estándar con Python
python sistema_calificaciones/02_Sistema_Calificaciones.py

# O utilizando el ejecutor uv
uv run sistema_calificaciones/02_Sistema_Calificaciones.py
```

### Opciones del Menú en Consola
```text
======================================================================
   SISTEMA DE CALIFICACIONES - SERVICIO NACIONAL DE APRENDIZAJE
   MÓDULO: MENÚ PRINCIPAL DE OPERACIONES
======================================================================

  [1] Registrar nuevo grupo de aprendices (Ingreso interactivo)
  [2] Cargar 5 casos de prueba predeterminados (Demostración inmediata)
  [3] Visualizar listado individual de calificaciones y promedios
  [4] Visualizar resumen estadístico y promedio general del grupo
  [5] Exportar registros a archivo plano (03_Registros_Calificaciones.txt)
  [6] Ejecutar traza de Prueba de Escritorio paso a paso
  [0] Salir del sistema
----------------------------------------------------------------------
```

---

## 📊 Caso de Demostración y Resultados Obtenidos

Al cargar los casos de prueba o digitar el grupo de demostración, el sistema produce los siguientes resultados consolidados:

### Listado Individual de Aprendices
| Documento | Aprendiz | Calificaciones | Promedio | Estado Académico |
| :---: | :--- | :---: | :---: | :---: |
| `1001` | Carlos Alberto Gómez | `[85.0, 90.0, 88.0, 92.0]` | **88.75** | ✅ Aprobado |
| `1002` | Ana María Rodríguez | `[60.0, 65.0, 70.0, 68.0]` | **65.75** | ❌ No Aprobado |
| `1003` | Julián David Vanegas | `[70.0, 70.0, 70.0, 70.0]` | **70.00** | ✅ Aprobado *(Frontera)* |
| `1004` | Jayzir Martínez | `[95.0, 98.0, 94.0, 100.0]` | **96.75** | ✅ Aprobado *(Excelente)* |
| `1005` | Laura Marcela Pérez | `[45.0, 50.0, 58.0, 52.0]` | **51.25** | ❌ No Aprobado |

### Estadísticas Consolidadas del Grupo
* **Total de Aprendices Evaluados:** 5
* **Sumatoria de Promedios:** 372.50
* **PROMEDIO GENERAL DEL GRUPO:** **74.50** (Supera el umbral institucional de 70.0)
* **Aprendices Aprobados:** 3 (60.0 %)
* **Aprendices No Aprobados:** 2 (40.0 %)
* **Calificación Promedio Más Alta:** **96.75** (*Jayzir Martínez*)
* **Calificación Promedio Más Baja:** **51.25** (*Laura Marcela Pérez*)

---

## 🛠️ Recompilación de Documentos Word (.DOCX)

Si se desea regenerar o personalizar los documentos DOCX institucionales con formato formal:

```bash
uv run --with python-docx python sistema_calificaciones/generar_documentos.py
```

---

## 👥 Equipo de Trabajo
- **Jayzir Martínez** ([@JayzirTech](https://github.com/JayzirTech))
- **Julián Vanegas**
