# -*- coding: utf-8 -*-
"""
GENERADOR DE DOCUMENTOS DOCX OFICIALES - SISTEMA DE CALIFICACIONES SENA
Genera con formato corporativo e institucional:
  - 01_Analisis_y_Diseno.docx
  - 04_Pruebas_y_Evidencias.docx
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

COLOR_NAVY = RGBColor(0x1B, 0x36, 0x5D)
COLOR_STEEL = RGBColor(0x2E, 0x5B, 0x88)
COLOR_TEXT = RGBColor(0x33, 0x33, 0x33)
COLOR_MUTED = RGBColor(0x66, 0x66, 0x66)
HEX_HEADER_BG = "1B365D"
HEX_ALT_ROW = "F8FAFC"
HEX_CALLOUT_BG = "F2F5F9"
HEX_BORDER = "CCCCCC"


def set_cell_background(cell, hex_color):
    """Establece color de fondo de celda."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos (padding) de celda en dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    if level == 1:
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
    elif level == 2:
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_STEEL
    elif level == 3:
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_STEEL
    return h


def apply_table_styles(tbl, col_widths, headers, rows_data):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], HEX_HEADER_BG)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    for r_idx, row_values in enumerate(rows_data):
        row_cells = tbl.add_row().cells
        bg_color = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_TEXT

    # Set column widths
    for row in tbl.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)


def create_callout_box(doc, text, title=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15

    if title:
        r_title = p.add_run(f"{title}\n")
        r_title.font.name = 'Calibri'
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = COLOR_NAVY

    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10)
    r_text.font.italic = True
    r_text.font.color.rgb = COLOR_TEXT


def setup_document_base():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_TEXT
    return doc


def add_document_header(doc, doc_code, doc_title, subtitle):
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE - SENA\nCENTRO DE COMERCIO Y SERVICIOS")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_MUTED

    p_code = doc.add_paragraph()
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(4)
    p_code.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_code = p_code.add_run(doc_code)
    r_code.font.name = 'Calibri'
    r_code.font.size = Pt(12)
    r_code.font.bold = True
    r_code.font.color.rgb = COLOR_STEEL

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(doc_title)
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    # Ficha de metadatos
    tbl_meta = doc.add_table(rows=1, cols=4)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [1.5, 2.0, 1.2, 1.8]
    headers = ["Programa", "ADSO - Lógica y Algoritmos", "Actividad", "Reto de Calificaciones"]
    apply_table_styles(tbl_meta, widths, ["Parámetro", "Detalle", "Entorno", "Integrantes"], [
        ["Proyecto", "Sistema de Calificaciones", "Lenguaje", "Python 3.13 / Pseudocódigo"],
        ["Modalidad", "Trabajo en Parejas", "Autores", "Jayzir Martínez & Julián Vanegas"],
        ["Condición", "Aprobación >= 70.0 Puntos", "Fecha", "Noviembre de 2026"]
    ])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def generar_docx_analisis_diseno(ruta_destino):
    doc = setup_document_base()
    add_document_header(
        doc,
        "01. DOCUMENTO DE ANÁLISIS Y DISEÑO LÓGICO",
        "Sistema de Registro y Procesamiento de Calificaciones",
        "Descomposición algorítmica, matriz E-P-S, diccionario de variables, estructuras de arreglos y pseudocódigo estructurado"
    )

    create_callout_box(
        doc,
        "Reto Principal: Una institución educativa necesita un algoritmo que permita registrar las calificaciones de varios aprendices, calcular el promedio de cada uno, determinar si aprobó o no (umbral institucional >= 70) y, al finalizar, mostrar el promedio general del grupo.",
        "ENUNCIADO DEL RETO FORMATIVO SENA"
    )

    add_styled_heading(doc, "1. Lectura y Comprensión de la Situación Problema", level=1)
    p = doc.add_paragraph(
        "El presente proyecto da solución a la necesidad operativa y académica de una institución formativa "
        "que requiere automatizar el procesamiento de calificaciones estudiantiles. La solución algorítmica captura "
        "las notas de cada aprendiz, determina su promedio aritmético exacto, evalúa la condición lógica de aprobación "
        "(promedio mayor o igual a 70 puntos) y produce al cierre un análisis consolidado con el promedio general del curso "
        "y métricas complementarias de rendimiento colectivo."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "2. Descomposición del Problema (Matriz E-P-S)", level=1)
    p_eps = doc.add_paragraph(
        "A través de la matriz de Entrada-Proceso-Salida (E-P-S) se aíslan las responsabilidades lógicas del sistema:"
    )
    p_eps.paragraph_format.line_spacing = 1.15

    tbl_eps = doc.add_table(rows=1, cols=3)
    apply_table_styles(
        tbl_eps,
        [2.0, 2.5, 2.0],
        ["ENTRADAS (Datos)", "PROCESOS (Algoritmo y Reglas)", "SALIDAS (Resultados)"],
        [
            [
                "• Cantidad de aprendices (N)\n• Número de notas por aprendiz (M)\n• Por cada aprendiz:\n  - Documento de identidad\n  - Nombre y apellidos\n  - Calificaciones (0.0 a 100.0)",
                "1. Validación de entradas (N>0, M>0, notas en [0, 100]).\n2. Ciclo exterior: iterar N aprendices.\n3. Ciclo interior: acumular notas del aprendiz.\n4. Promedio individual = Suma / M.\n5. Decisión: Si Promedio >= 70 -> Aprobado; Sino -> No Aprobado.\n6. Acumular promedios al grupo.\n7. Promedio General = Suma Grupal / N.\n8. Conteo de aprobados y porcentajes.",
                "• Boletín individual por consola con notas, promedio y estado.\n• Promedio general del grupo.\n• Conteo y porcentaje de aprobación/no aprobación.\n• Aprendices con calificación máxima y mínima.\n• Archivo plano estructurado '03_Registros_Calificaciones.txt'."
            ]
        ]
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_styled_heading(doc, "3. Diccionario y Especificación de Variables", level=1)
    tbl_vars = doc.add_table(rows=1, cols=4)
    apply_table_styles(
        tbl_vars,
        [1.5, 1.1, 1.1, 2.8],
        ["Variable", "Tipo de Dato", "Ámbito", "Descripción y Rol Algorítmico"],
        [
            ["UMBRAL_APROBACION", "Real (Constante)", "Global", "Constante de negocio fijada en 70.0 puntos."],
            ["num_aprendices (N)", "Entero", "Global", "Cantidad de estudiantes a procesar (N >= 1)."],
            ["num_notas (M)", "Entero", "Global", "Número de calificaciones por estudiante (M >= 1)."],
            ["i, j", "Entero", "Local", "Variables de control de ciclos exterior e interior."],
            ["id_doc, nombre", "Cadena", "Local", "Identificación y nombre completo del aprendiz."],
            ["nota_actual", "Real", "Local", "Nota individual validada en el rango 0.0 a 100.0."],
            ["suma_indiv", "Real", "Local", "Acumulador de las notas de un aprendiz específico."],
            ["prom_indiv", "Real", "Local", "Promedio individual = suma_indiv / num_notas."],
            ["estados[i]", "Cadena", "Global", "Veredicto del aprendiz ('Aprobado' / 'No Aprobado')."],
            ["acum_general", "Real", "Global", "Acumulador de todos los promedios del grupo."],
            ["prom_general", "Real", "Global", "Promedio global = acum_general / num_aprendices."],
            ["cont_aprobados", "Entero", "Global", "Contador de aprendices con promedio >= 70.0."],
            ["cont_no_aprobados", "Entero", "Global", "Contador de aprendices con promedio < 70.0."]
        ]
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_styled_heading(doc, "4. Identificación y Justificación de Arreglos", level=1)
    p_arr = doc.add_paragraph(
        "El sistema modela la información en arreglos unidimensionales (vectores) y bidimensionales (matrices) "
        "con los siguientes fundamentos pedagógicos y computacionales:\n"
        "1. Matriz de Calificaciones (matriz_calificaciones[N][M]): Permite retener cada nota de cada aprendiz "
        "en memoria para auditoría y visualización completa.\n"
        "2. Vectores Paralelos (documentos[], nombres[], promedios[], estados[]): Vinculan cada atributo del aprendiz "
        "mediante su índice ordinal i (0 a N-1).\n"
        "3. Justificación Técnica: El uso de arreglos desacopla la fase de captura de la fase de análisis. "
        "Permite volver a consultar las notas, recalcular estadísticas o exportar reportes sin obligar al usuario "
        "a volver a digitar los registros, garantizando una complejidad de acceso O(1)."
    )
    p_arr.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "5. Algoritmo en Pseudocódigo Estructurado (Estándar SENA)", level=1)
    pseudocodigo_texto = (
        "Algoritmo SistemaRegistroCalificaciones\n"
        "    Definir num_aprendices, num_notas, i, j Como Entero\n"
        "    Definir suma_indiv, prom_indiv, acum_general, prom_general Como Real\n"
        "    Definir cont_aprob, cont_reprob Como Entero\n"
        "    UMBRAL_APROBACION <- 70.0\n\n"
        "    Repetir Leer num_aprendices Hasta Que num_aprendices > 0\n"
        "    Repetir Leer num_notas Hasta Que num_notas > 0\n\n"
        "    Dimension nombres[num_aprendices], notas[num_aprendices, num_notas]\n"
        "    Dimension promedios[num_aprendices], estados[num_aprendices]\n\n"
        "    acum_general <- 0.0; cont_aprob <- 0; cont_reprob <- 0\n\n"
        "    Para i <- 1 Hasta num_aprendices Hacer\n"
        "        Leer nombres[i]\n"
        "        suma_indiv <- 0.0\n"
        "        Para j <- 1 Hasta num_notas Hacer\n"
        "            Repetir Leer notas[i, j] Hasta Que notas[i, j] >= 0 Y notas[i, j] <= 100\n"
        "            suma_indiv <- suma_indiv + notas[i, j]\n"
        "        FinPara\n"
        "        prom_indiv <- suma_indiv / num_notas\n"
        "        promedios[i] <- prom_indiv\n\n"
        "        // Estructura de Decisión Lógica (Acción 6)\n"
        "        Si prom_indiv >= UMBRAL_APROBACION Entonces\n"
        "            estados[i] <- 'Aprobado'\n"
        "            cont_aprob <- cont_aprob + 1\n"
        "        Sino\n"
        "            estados[i] <- 'No Aprobado'\n"
        "            cont_reprob <- cont_reprob + 1\n"
        "        FinSi\n"
        "        acum_general <- acum_general + prom_indiv\n"
        "    FinPara\n\n"
        "    // Cálculo del Promedio General del Grupo (Acción 7)\n"
        "    prom_general <- acum_general / num_aprendices\n"
        "    Escribir 'PROMEDIO GENERAL DEL GRUPO: ', prom_general\n"
        "FinAlgoritmo"
    )
    create_callout_box(doc, pseudocodigo_texto, "PSEUDOCÓDIGO FORMAL PSeInt / SENA")

    doc.save(ruta_destino)
    print(f"[OK] Archivo generado: {ruta_destino}")


def generar_docx_pruebas_evidencias(ruta_destino):
    doc = setup_document_base()
    add_document_header(
        doc,
        "04. INFORME DE PRUEBAS DE ESCRITORIO Y CALIDAD",
        "Pruebas de Escritorio, Traza de Variables y Bitácora de Errores",
        "Verificación formal paso a paso, análisis en frontera, pruebas de robustez y resolución de discrepancias"
    )

    create_callout_box(
        doc,
        "Acción 8: Realizar pruebas de escritorio con diferentes datos, revisar los resultados y corregir los errores encontrados. Validación exhaustiva del flujo algorítmico, límites de decisión y precisión numérica.",
        "PROPÓSITO DE ASEGURAMIENTO DE CALIDAD"
    )

    add_styled_heading(doc, "1. Justificación de la Prueba de Escritorio", level=1)
    p = doc.add_paragraph(
        "La prueba de escritorio permite auditar la validez matemática y lógica del algoritmo de forma previa "
        "o independiente a su ejecución computacional. Se monitorean sistemáticamente las asignaciones en memoria, "
        "el comportamiento de los acumuladores, los contadores de control y el salto de flujo en las estructuras condicionales."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "2. Escenario 1: Traza Formal Paso a Paso (3 Aprendices, 3 Notas)", level=1)
    tbl_traza = doc.add_table(rows=1, cols=9)
    apply_table_styles(
        tbl_traza,
        [0.5, 0.5, 1.4, 0.8, 0.8, 0.8, 0.9, 0.8, 0.8],
        ["Paso", "i", "Aprendiz", "Notas", "Suma", "Prom", "Estado", "Acum", "P. Gral"],
        [
            ["1", "1", "Carlos Gómez", "80, 75, 85", "240.0", "80.00", "Aprobado", "80.00", "-"],
            ["2", "2", "Ana Rodríguez", "60, 65, 70", "195.0", "65.00", "No Aprobado", "145.00", "-"],
            ["3", "3", "Julián Vanegas", "70, 70, 70", "210.0", "70.00", "Aprobado", "215.00", "-"],
            ["Fin", "-", "TOTAL GRUPO", "9 Notas", "645.0", "-", "2 Ap / 1 Rep", "215.00", "71.67"]
        ]
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_styled_heading(doc, "3. Escenarios Críticos Evaluados", level=1)
    p_scen = doc.add_paragraph(
        "• Escenario en Límite Exacto (Frontera 70.0): Un aprendiz con notas [70.0, 70.0, 70.0] promedia 70.00. "
        "El operador relacional '>=' garantiza que obtenga el estado 'Aprobado'. Un caso con 69.67 obtiene 'No Aprobado'.\n"
        "• Escenario de Valores Extremos: Se probaron combinaciones con notas perfectas (100.0) y notas mínimas (0.0). "
        "El algoritmo mantuvo la integridad sin errores de desbordamiento de coma flotante.\n"
        "• Escenario de Robustez: Ingreso de texto, números negativos y notas mayores a 100 fueron interceptados "
        "por las funciones de validación defensiva, solicitando el reingreso sin interrumpir el flujo."
    )
    p_scen.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "4. Bitácora de Errores Encontrados y Correcciones", level=1)
    tbl_errores = doc.add_table(rows=1, cols=4)
    apply_table_styles(
        tbl_errores,
        [1.3, 1.8, 1.8, 1.6],
        ["Error Detectado", "Causa Raíz", "Efecto Observado", "Solución Aplicada"],
        [
            [
                "Acumulador no reiniciado",
                "suma_indiv colocado fuera del ciclo 'Para i'.",
                "Las notas del siguiente aprendiz se sumaban al anterior.",
                "Reubicación de suma_indiv <- 0 al iniciar cada aprendiz."
            ],
            [
                "Operador estricto '>' en vez de '>='",
                "Condición 'promedio > 70.0'.",
                "Aprendices con exactamente 70.0 quedaban como 'No Aprobados'.",
                "Ajuste del operador relacional a 'promedio >= 70.0'."
            ],
            [
                "División por cero en grupo vacío",
                "Sin validación de N >= 1.",
                "Colapso del programa al dividir entre 0 aprendices.",
                "Bucle 'Repetir...Hasta Que N > 0' y validación defensiva."
            ],
            [
                "Fallo por coma decimal (ej: 85,5)",
                "Python exige punto flotante (.)",
                "Excepción de tipo ValueError al convertir entrada.",
                "Estandarización automática con .replace(',', '.')."
            ]
        ]
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_styled_heading(doc, "5. Conclusiones y Respaldo Institucional", level=1)
    p_conc = doc.add_paragraph(
        "El ciclo completo de desarrollo, modelado de variables, diseño de pseudocódigo y pruebas de escritorio "
        "demuestra que el sistema satisface plenamente los 8 requerimientos de la actividad formativa. "
        "El software y la documentación adjunta quedan listos para sustentación individual y colectiva ante el comité formativo del SENA."
    )
    p_conc.paragraph_format.line_spacing = 1.15

    doc.save(ruta_destino)
    print(f"[OK] Archivo generado: {ruta_destino}")


def main():
    carpeta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_analisis = os.path.join(carpeta_base, "01_Analisis_y_Diseno.docx")
    ruta_pruebas = os.path.join(carpeta_base, "04_Pruebas_y_Evidencias.docx")

    print("Generando documentos institucionales DOCX...")
    generar_docx_analisis_diseno(ruta_analisis)
    generar_docx_pruebas_evidencias(ruta_pruebas)
    print("¡Todos los documentos han sido creados con éxito!")


if __name__ == "__main__":
    main()
