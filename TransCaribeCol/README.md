# Sistema de Nómina y Honorarios - TransCaribeCol S.C.A.

> **Actividad 3.4: Reto de Desarrollo - Módulo de Nómina**  
> **Servicio Nacional de Aprendizaje (SENA) - Centro de Comercio y Servicios**  
> **Equipo de Desarrollo:** Julián Vanegas & Jayzir Martínez  
> **Modalidad:** Trabajo en Parejas (Distribución de roles: Programación, Documentación, Análisis Normativo y Validación)  
> **Conformidad Legal:** 100% Código Sustantivo del Trabajo (CST), Ley 100 de 1993 y Ley 1955 de 2019.

---

## 1. Descripción del Proyecto

La empresa **Transportes del Gran Caribe Colombiano S.C.A. (TransCaribeCol)** requería un sistema de información de consola desarrollado en Python para procesar la nómina mensual y la cuenta de honorarios de su talento humano, discriminando con precisión técnica y jurídica las dos modalidades de contratación presentes en la compañía:

1. **Personal Administrativo:** Contrato laboral dependiente regido por el **Código Sustantivo del Trabajo (CST)**.
2. **Personal Operativo:** Contrato de prestación de servicios por honorarios (OPS) regido por la **Ley 100 de 1993** y el **Art. 244 de la Ley 1955 de 2019** (Conductores, Oficios Generales y Vigilancia).

La solución entrega comprobantes individuales en pantalla, un resumen consolidado de liquidaciones y persistencia de datos en el archivo estructurado `03_Registros_Nomina.txt`.

---

## 2. Estructura de Entregables Oficiales

El repositorio contiene todos los archivos solicitados en la **Tabla 3** de la guía oficial:

| Archivo | Formato | Descripción / Contenido |
| :--- | :---: | :--- |
| **`01_Analisis_y_Diseno.docx`** | DOCX | Documento formal con la descripción del problema, matriz E-P-S, análisis normativo del CST/Ley 100, tabla de reglas, algoritmo en pseudocódigo y diccionario de variables. |
| **`02_Programa_Nomina.py`** | Python (.py) | Código fuente modular, ejecutable y documentado con menú interactivo, validación de excepciones y algoritmos de liquidación. |
| **`03_Registros_Nomina.txt`** | TXT Plano | Archivo generado por el programa con la tabla de liquidaciones, columnas alineadas y sumatorias de control. |
| **`04_Pruebas_y_Evidencias.docx`** | DOCX | Informe de aseguramiento de calidad con los 4 escenarios obligatorios de la guía, resultados esperados vs. obtenidos, bitácora de correcciones y guía de sustentación individual. |
| **`README.md`** | Markdown | Guía técnica y operativa del proyecto. |

---

## 3. Marco Normativo y Reglas de Negocio Implementadas

### A. Personal Administrativo (Relación Laboral Dependiente - CST)
- **Tarifa Base Ordinaria:** $20.000 / hora trabajada.
- **Horas Extras (HE):** $25.000 / hora (computan para devengados y base de prestaciones).
- **Aportes a Salud:** 4,0% a cargo del trabajador (deducido de nómina).
- **Aportes a Pensión:** 4,0% a cargo del trabajador (deducido de nómina).
- **ARL (Riesgo I - 0,522%):** Aporte asumido al 100% por el **empleador** según el Decreto 1072 de 2015. No se le descuenta al empleado; se reporta de forma informativa en el comprobante.
- **Fórmula Neto a Pagar:**  
  $$\text{Neto} = \text{Total Devengado} - (\text{Salud}_{4\%} + \text{Pensión}_{4\%})$$

### B. Personal Operativo (Contratistas Independientes - Ley 100 / Ley 1955)
- **Tarifa por Hora:** $40.000 / hora pactada.
- **Asignación Mensual de Horas según Cargo:**
  - **Conductor:** 160 horas mensuales $\rightarrow$ Honorarios brutos: **$6.400.000**
  - **Oficios Generales:** 100 horas mensuales $\rightarrow$ Honorarios brutos: **$4.000.000**
  - **Vigilancia:** 336 horas mensuales $\rightarrow$ Honorarios brutos: **$13.440.000**
- **Ingreso Base de Cotización (IBC):** **40%** del valor mensual bruto facturado (Art. 244 Ley 1955 de 2019).
- **Deducciones de Seguridad Social (a cargo del contratista):**
  - **Salud:** 12,5% sobre el IBC.
  - **Pensión:** 16,0% sobre el IBC.
  - **ARL sobre IBC según Nivel de Riesgo:**
    - *Oficios Generales:* Riesgo I = **0,522%**
    - *Conductor:* Riesgo II = **1,044%**
    - *Vigilancia:* Riesgo IV = **4,350%**
- **Fórmula Neto a Pagar:**  
  $$\text{Neto} = \text{Honorarios Brutos} - (\text{Salud}_{12.5\%} + \text{Pensión}_{16\%} + \text{ARL}_{\text{Riesgo}})$$

---

## 4. Instrucciones de Ejecución

### Requisitos Previos
- Python 3.8 o superior (compatible con Python 3.13).
- No requiere dependencias externas para su ejecución habitual (usa biblioteca estándar de Python).

### Comandos de Ejecución

Desde la terminal en el directorio del proyecto:

```bash
# Ejecución estándar con Python
python 02_Programa_Nomina.py

# O utilizando uv (si está disponible en el entorno)
uv run 02_Programa_Nomina.py
```

### Opciones del Menú Principal
1. **Registrar nuevo trabajador y calcular nómina:** Solicita datos, valida tipos numéricos y muestra comprobante individual de inmediato.
2. **Mostrar resumen consolidado en pantalla:** Presenta la matriz de trabajadores en consola en formato tabular.
3. **Guardar registros en archivo TXT:** Exporta los registros a `03_Registros_Nomina.txt` con encabezados y totales.
4. **Consultar archivo TXT existente:** Lee y despliega el contenido actual del archivo persistido.
5. **Cargar los 4 casos de prueba de la guía:** Precarga automáticamente los trabajadores de prueba para verificación instantánea.
6. **Salir:** Finaliza la sesión de manera segura.

---

## 5. Tabla de Liquidación de Casos de Prueba Oficiales

Los 4 casos de prueba exigidos por la instructora arrojaron los siguientes resultados auditados:

| Nombre | Tipo | Cargo | HT | Salario | HE | TPHE | Salud | Pensión | ARL | Total a Pagar |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Carlos Mendoza** | Administrativo | Asistente Contable | 160 | $3.200.000 | 10 | $250.000 | $138.000 | $138.000 | $18.009* | **$3.174.000** |
| **Andrés Restrepo** | Operativo | Conductor | 160 | $6.400.000 | 0 | $0 | $320.000 | $409.600 | $26.726 | **$5.643.674** |
| **María Gómez** | Operativo | Oficios Generales | 100 | $4.000.000 | 0 | $0 | $200.000 | $256.000 | $8.352 | **$3.535.648** |
| **Jorge Morales** | Operativo | Vigilancia | 336 | $13.440.000 | 0 | $0 | $672.000 | $860.160 | $233.856 | **$11.673.984** |
| **TOTALES** | - | - | - | **$27.040.000** | - | **$250.000** | **$1.330.000** | **$1.663.760** | **$286.943** | **$24.027.306** |

*\*Nota: Para Carlos Mendoza (Administrativo), el valor de ARL ($18.009) corresponde al aporte patronal legal y no fue descontado de su salario neto.*

---

## 6. Claves para la Sustentación Individual (Rol Documentador)

Como encargado del rol de **Documentación y Modelado**, ten presentes estos cuatro pilares clave ante las preguntas de la instructora:
1. **Diferenciación Jurídica:** El sistema no trata a todos por igual porque la ley colombiana no lo permite: el personal administrativo tiene contrato de trabajo (CST) y paga 4% en salud y pensión; los operativos son contratistas independientes (Ley 1955) que cotizan sobre el 40% de IBC y asumen la totalidad de su seguridad social.
2. **Manejo de Errores:** Se implementó una defensa robusta de entradas: bucles de validación para nombres no vacíos y bloques `try-except` para evitar que horas negativas o letras dañen la ejecución.
3. **Estructura en Memoria:** Se empleó una lista de diccionarios que actúa como una matriz bidimensional estructurada, lo que permite ordenar la información para el comprobante y para la tabla consolidada.
4. **Persistencia Transparente:** La función de exportación a `03_Registros_Nomina.txt` escribe en formato tabular con codificación UTF-8, asegurando que los reportes puedan ser leídos por cualquier auditor o sistema externo.
