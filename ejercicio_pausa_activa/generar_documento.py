import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Establece el color de fondo de una celda."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos (padding) de una celda en dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    if level == 1:
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) # Azul Marino Profundo
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x2E, 0x5B, 0x88)
    return h

def main():
    doc = Document()
    
    # Configuración de márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Estilo Normal predeterminado
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # --- Título Principal ---
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("Taller de Algoritmos y Lógica de Programación")
    run_title.font.size = Pt(13)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(4)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_h1 = h1.add_run("Solución: Compra para una pausa activa")
    run_h1.font.size = Pt(19)
    run_h1.font.bold = True
    run_h1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Guía detallada de desarrollo paso a paso y código complementario")
    run_sub.font.size = Pt(10.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
    
    # --- Caja de Enunciado ---
    callout_tbl = doc.add_table(rows=1, cols=1)
    callout_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    callout_tbl.autofit = False
    callout_tbl.columns[0].width = Inches(6.5)
    
    cell = callout_tbl.cell(0, 0)
    set_cell_background(cell, "F2F5F9")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    callout_p = cell.paragraphs[0]
    callout_p.paragraph_format.space_before = Pt(2)
    callout_p.paragraph_format.space_after = Pt(2)
    callout_p.paragraph_format.line_spacing = 1.15
    run_enunc_lbl = callout_p.add_run("Enunciado del problema:\n")
    run_enunc_lbl.bold = True
    run_enunc_lbl.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    run_enunc_lbl.font.size = Pt(10.5)
    
    run_enunc_txt = callout_p.add_run(
        "«Una persona compra 3 botellas de agua a $2.500 cada una y 2 frutas a $1.800 cada una. "
        "La tienda ofrece un descuento de $1.000 sobre el subtotal si la compra es de $10.000 o más. "
        "Diseña los pasos para calcular el total que debe pagar. No necesitas programar en un lenguaje específico. Puedes usar Python.»"
    )
    run_enunc_txt.font.size = Pt(10.5)
    run_enunc_txt.font.italic = True
    
    # Separador
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # --- 1. IDENTIFICACIÓN DE ENTRADAS, PROCESO Y SALIDA ---
    add_heading_styled(doc, "1. Identificación de Entradas, Proceso y Salida", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Todo problema computacional o algorítmico se estructura en tres fases fundamentales:")
    
    # Subsección Entradas
    p_in = doc.add_paragraph(style='List Bullet')
    p_in.paragraph_format.space_after = Pt(3)
    r = p_in.add_run("Entradas (Datos iniciales necesarios):")
    r.bold = True
    
    p1 = doc.add_paragraph(style='List Bullet 2')
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run("Cantidad de botellas de agua compradas (ej. 3).")
    
    p2 = doc.add_paragraph(style='List Bullet 2')
    p2.paragraph_format.space_after = Pt(2)
    p2.add_run("Precio unitario de una botella de agua ($2.500).")
    
    p3 = doc.add_paragraph(style='List Bullet 2')
    p3.paragraph_format.space_after = Pt(2)
    p3.add_run("Cantidad de frutas compradas (ej. 2).")
    
    p4 = doc.add_paragraph(style='List Bullet 2')
    p4.paragraph_format.space_after = Pt(2)
    p4.add_run("Precio unitario de una fruta ($1.800).")
    
    p5 = doc.add_paragraph(style='List Bullet 2')
    p5.paragraph_format.space_after = Pt(2)
    p5.add_run("Umbral mínimo para acceder al beneficio del descuento ($10.000).")
    
    p6 = doc.add_paragraph(style='List Bullet 2')
    p6.paragraph_format.space_after = Pt(4)
    p6.add_run("Monto fijo del descuento aplicable ($1.000).")
    
    # Subsección Proceso
    p_proc = doc.add_paragraph(style='List Bullet')
    p_proc.paragraph_format.space_after = Pt(3)
    r = p_proc.add_run("Proceso (Operaciones de cálculo y toma de decisiones):")
    r.bold = True
    
    proc_steps = [
        "Calcular el costo parcial de las botellas: Cantidad de botellas × Precio unitario del agua.",
        "Calcular el costo parcial de las frutas: Cantidad de frutas × Precio unitario de la fruta.",
        "Calcular el subtotal de la compra: Sumar el costo total de botellas más el costo total de frutas.",
        "Evaluar la condición condicional: Verificar si el subtotal es mayor o igual a $10.000.",
        "Calcular el monto final: Si la condición se cumple, restar $1.000 al subtotal; de lo contrario, el total se mantiene idéntico al subtotal."
    ]
    for step in proc_steps:
        ps = doc.add_paragraph(style='List Bullet 2')
        ps.paragraph_format.space_after = Pt(2)
        ps.add_run(step)
        
    # Subsección Salida
    p_out = doc.add_paragraph(style='List Bullet')
    p_out.paragraph_format.space_after = Pt(3)
    r = p_out.add_run("Salida (Resultados producidos):")
    r.bold = True
    
    out_items = [
        "El total final a pagar por el cliente.",
        "Información de soporte (opcional pero recomendada): Subtotal calculado y valor del descuento aplicado ($0 o $1.000)."
    ]
    for item in out_items:
        po = doc.add_paragraph(style='List Bullet 2')
        po.paragraph_format.space_after = Pt(2)
        po.add_run(item)
        
    # --- 2. PASOS EN LENGUAJE NATURAL (ALGORITMO) ---
    add_heading_styled(doc, "2. Pasos en Lenguaje Natural (Algoritmo Secuencial)", level=1)
    
    intro_algo = doc.add_paragraph()
    intro_algo.paragraph_format.space_after = Pt(4)
    intro_algo.add_run("A continuación se describen las instrucciones en el orden cronológico estricto en que deben ejecutarse:")
    
    pasos = [
        ("Definición de tarifas:", " Establecer los precios unitarios fijos: $2.500 por cada botella de agua y $1.800 por cada fruta."),
        ("Captura de compras:", " Determinar las cantidades adquiridas por el cliente (3 botellas de agua y 2 frutas)."),
        ("Subtotal de botellas:", " Multiplicar la cantidad de botellas por su precio unitario ($2.500)."),
        ("Subtotal de frutas:", " Multiplicar la cantidad de frutas por su precio unitario ($1.800)."),
        ("Cálculo del subtotal general:", " Sumar el costo obtenido de las botellas y el costo de las frutas."),
        ("Verificación de la regla de descuento:", " Comparar el subtotal con el límite de la promoción ($10.000):"),
        ("Determinación del total:", " Si el subtotal es mayor o igual a $10.000, restar $1.000 al subtotal. Si es menor, conservar el subtotal sin cambios."),
        ("Presentación de resultados:", " Informar y mostrar el total definitivo a pagar al cliente.")
    ]
    
    for i, (bold_txt, regular_txt) in enumerate(pasos, start=1):
        p_step = doc.add_paragraph()
        p_step.paragraph_format.left_indent = Inches(0.25)
        p_step.paragraph_format.space_after = Pt(3)
        r_num = p_step.add_run(f"Paso {i}. ")
        r_num.bold = True
        r_num.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_title = p_step.add_run(bold_txt)
        r_title.bold = True
        p_step.add_run(regular_txt)

    # --- 3. VARIABLES Y NOMBRES CLAROS ---
    add_heading_styled(doc, "3. Identificación y Definición de Variables", level=1)
    
    p_var = doc.add_paragraph()
    p_var.paragraph_format.space_after = Pt(6)
    p_var.add_run("Se proponen nombres descriptivos siguiendo el estándar formal (convención snake_case):")
    
    # Crear Tabla
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Anchos de columna
    col_widths = [Inches(1.8), Inches(1.1), Inches(1.0), Inches(2.6)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w
        
    # Encabezados
    headers = ["Nombre de Variable", "Tipo de Dato", "Rol / Ámbito", "Descripción del Contenido"]
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p_hdr = hdr_cells[i].paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_hdr.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    data_variables = [
        ("precio_botella", "Entero / Real", "Constante", "Precio unitario fijado para el agua ($2.500)"),
        ("precio_fruta", "Entero / Real", "Constante", "Precio unitario fijado para la fruta ($1.800)"),
        ("umbral_descuento", "Entero / Real", "Constante", "Monto mínimo para aplicar descuento ($10.000)"),
        ("valor_descuento", "Entero / Real", "Constante", "Importe que se descuenta al cumplir la regla ($1.000)"),
        ("cantidad_botellas", "Entero", "Variable (Entrada)", "Número de botellas de agua que adquiere el cliente"),
        ("cantidad_frutas", "Entero", "Variable (Entrada)", "Número de frutas que adquiere el cliente"),
        ("costo_botellas", "Entero / Real", "Variable (Cálculo)", "Gasto correspondiente solo a las botellas"),
        ("costo_frutas", "Entero / Real", "Variable (Cálculo)", "Gasto correspondiente solo a las frutas"),
        ("subtotal", "Entero / Real", "Variable (Cálculo)", "Suma acumulada antes de evaluar beneficios"),
        ("descuento_aplicado", "Entero / Real", "Variable (Cálculo)", "Valor real descontado ($0 o $1.000)"),
        ("total_pagar", "Entero / Real", "Variable (Salida)", "Monto neto final que debe cancelar el comprador")
    ]
    
    for row_idx, data in enumerate(data_variables):
        row = table.add_row()
        bg_col = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(data):
            c = row.cells[i]
            c.width = col_widths[i]
            set_cell_background(c, bg_col)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p_cell = c.paragraphs[0]
            p_cell.paragraph_format.space_after = Pt(0)
            p_cell.paragraph_format.space_before = Pt(0)
            r = p_cell.add_run(val)
            r.font.size = Pt(9.5)
            if i == 0:
                r.font.name = 'Consolas'
                r.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            elif i in (1, 2):
                p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 4. CÁLCULO PARA LOS DATOS DEL ENUNCIADO ---
    add_heading_styled(doc, "4. Cálculo para los Datos del Enunciado (Caso Principal)", level=1)
    
    p_c4 = doc.add_paragraph()
    p_c4.paragraph_format.space_after = Pt(4)
    p_c4.add_run("Se evalúa la compra establecida en el problema: ")
    r = p_c4.add_run("3 botellas de agua y 2 frutas.")
    r.bold = True
    
    calc_steps = [
        ("Cálculo botellas de agua:", " 3 × $2.500 = $7.500"),
        ("Cálculo frutas:", " 2 × $1.800 = $3.600"),
        ("Cálculo del subtotal:", " $7.500 + $3.600 = $11.100"),
        ("Evaluación de la condición de descuento:", " ¿$11.100 ≥ $10.000? ")
    ]
    for title_s, val_s in calc_steps:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(2)
        r_t = p_s.add_run(title_s)
        r_t.bold = True
        p_s.add_run(val_s)
        if "¿$11.100 ≥ $10.000?" in val_s:
            r_bool = p_s.add_run("VERDADERO (SÍ).")
            r_bool.bold = True
            r_bool.font.color.rgb = RGBColor(0x27, 0x7E, 0x27)
            p_s.add_run(" Por lo tanto, se aplica el descuento de $1.000.")

    # Caja de Resultado Caso 1
    res1_tbl = doc.add_table(rows=1, cols=1)
    res1_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    res1_tbl.autofit = False
    res1_tbl.columns[0].width = Inches(6.5)
    c1 = res1_tbl.cell(0, 0)
    set_cell_background(c1, "EBF3E8") # Verde claro
    set_cell_margins(c1, top=120, bottom=120, left=160, right=160)
    p_c1 = c1.paragraphs[0]
    p_c1.paragraph_format.space_before = Pt(2)
    p_c1.paragraph_format.space_after = Pt(2)
    r1_l = p_c1.add_run("Total a pagar: ")
    r1_l.font.size = Pt(11)
    r1_l.bold = True
    p_c1.add_run("$11.100 - $1.000 = ")
    r1_val = p_c1.add_run("$10.100\n")
    r1_val.font.size = Pt(13)
    r1_val.bold = True
    r1_val.font.color.rgb = RGBColor(0x1E, 0x62, 0x1E)
    r1_conc = p_c1.add_run("Conclusión: El cliente obtiene el beneficio y paga un total de $10.100.")
    r1_conc.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 5. PRUEBA DE OTRO CASO ---
    add_heading_styled(doc, "5. Prueba de Otro Caso: 2 Botellas y 1 Fruta", level=1)
    
    p_c5 = doc.add_paragraph()
    p_c5.paragraph_format.space_after = Pt(4)
    p_c5.add_run("Se evalúa un escenario con una canasta de compra inferior:")
    
    calc_steps_2 = [
        ("Cálculo botellas de agua:", " 2 × $2.500 = $5.000"),
        ("Cálculo frutas:", " 1 × $1.800 = $1.800"),
        ("Cálculo del subtotal:", " $5.000 + $1.800 = $6.800"),
        ("Evaluación de la condición de descuento:", " ¿$6.800 ≥ $10.000? ")
    ]
    for title_s, val_s in calc_steps_2:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(2)
        r_t = p_s.add_run(title_s)
        r_t.bold = True
        p_s.add_run(val_s)
        if "¿$6.800 ≥ $10.000?" in val_s:
            r_bool = p_s.add_run("FALSO (NO).")
            r_bool.bold = True
            r_bool.font.color.rgb = RGBColor(0xA6, 0x1C, 0x1C)
            p_s.add_run(" Por lo tanto, el descuento aplicado es de $0.")

    # Caja de Resultado Caso 2
    res2_tbl = doc.add_table(rows=1, cols=1)
    res2_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    res2_tbl.autofit = False
    res2_tbl.columns[0].width = Inches(6.5)
    c2 = res2_tbl.cell(0, 0)
    set_cell_background(c2, "FDEEE9") # Naranja/rojo claro
    set_cell_margins(c2, top=120, bottom=120, left=160, right=160)
    p_c2 = c2.paragraphs[0]
    p_c2.paragraph_format.space_before = Pt(2)
    p_c2.paragraph_format.space_after = Pt(2)
    r2_q = p_c2.add_run("¿Se aplica el descuento? ")
    r2_q.bold = True
    r2_ans = p_c2.add_run("NO SE APLICA.\n")
    r2_ans.bold = True
    r2_ans.font.color.rgb = RGBColor(0x99, 0x22, 0x00)
    r2_l = p_c2.add_run("Total a pagar: ")
    r2_l.bold = True
    p_c2.add_run("Total = Subtotal = ")
    r2_val = p_c2.add_run("$6.800\n")
    r2_val.font.size = Pt(13)
    r2_val.bold = True
    r2_val.font.color.rgb = RGBColor(0x99, 0x22, 0x00)
    r2_conc = p_c2.add_run("Conclusión: Debido a que $6.800 no alcanza el monto mínimo fijado de $10.000, el comprador debe pagar el valor exacto de su compra sin rebajas.")
    r2_conc.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 6. PREGUNTAS SOBRE REGLAS NO CLARAS ---
    add_heading_styled(doc, "6. Preguntas para Clarificar Reglas de Negocio", level=1)
    
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_after = Pt(4)
    p_q.add_run(
        "En la ingeniería de requisitos y desarrollo de algoritmos, identificar posibles ambigüedades es crucial para evitar errores en producción. "
        "A continuación se plantean preguntas clave que deberían realizarse al cliente o responsable de negocio:"
    )
    
    preguntas = [
        ("Pregunta principal (Acumulación del beneficio):",
         " «¿El descuento de $1.000 se aplica una única vez por transacción cuando se superan los $10.000, o es acumulativo/proporcional por cada $10.000 consumidos (por ejemplo, $2.000 de descuento si la cuenta llega a $20.000 o más)?»"),
        ("Pregunta secundaria (Tratamiento fiscal / IVA):",
         " «¿El umbral de los $10.000 y el descuento de $1.000 se evalúan sobre el precio bruto antes de impuestos o sobre el valor neto que incluye el IVA?»"),
        ("Pregunta secundaria (Combinación con otros productos o promociones):",
         " «Si el cliente compra artículos de otras categorías de la tienda que ya posean otra oferta, ¿esos montos suman para alcanzar los $10.000 o la promoción es exclusiva para botellas y frutas?»")
    ]
    
    for tit, texto in preguntas:
        pq = doc.add_paragraph(style='List Bullet')
        pq.paragraph_format.space_after = Pt(3)
        rt = pq.add_run(tit)
        rt.bold = True
        rt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pq.add_run(texto)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- SECCIÓN EXTRA: IMPLEMENTACIÓN EN PYTHON ---
    add_heading_styled(doc, "Anexo: Implementación de Referencia en Python", level=1)
    
    p_py = doc.add_paragraph()
    p_py.paragraph_format.space_after = Pt(4)
    p_py.add_run("El siguiente script en Python plasma fielmente el modelo lógico planteado:")
    
    python_code = '''# Constantes del modelo comercial
PRECIO_BOTELLA = 2500
PRECIO_FRUTA = 1800
UMBRAL_DESCUENTO = 10000
VALOR_DESCUENTO = 1000

def calcular_compra(cantidad_botellas: int, cantidad_frutas: int) -> dict:
    """
    Calcula el subtotal, el descuento aplicable y el total a pagar.
    """
    # 1. Proceso de cálculo de costos
    costo_botellas = cantidad_botellas * PRECIO_BOTELLA
    costo_frutas = cantidad_frutas * PRECIO_FRUTA
    subtotal = costo_botellas + costo_frutas
    
    # 2. Evaluación condicional de la regla de descuento
    if subtotal >= UMBRAL_DESCUENTO:
        descuento = VALOR_DESCUENTO
        aplica_descuento = True
    else:
        descuento = 0
        aplica_descuento = False
        
    total_pagar = subtotal - descuento
    
    return {
        "subtotal": subtotal,
        "descuento": descuento,
        "total_pagar": total_pagar,
        "aplica_descuento": aplica_descuento
    }

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    # Caso 1: 3 botellas y 2 frutas
    c1 = calcular_compra(3, 2)
    print("--- CASO 1 (3 botellas, 2 frutas) ---")
    print(f"Subtotal: ${c1['subtotal']:,}")
    print(f"Descuento: ${c1['descuento']:,}")
    print(f"Total a pagar: ${c1['total_pagar']:,}\\n")
    
    # Caso 2: 2 botellas y 1 fruta
    c2 = calcular_compra(2, 1)
    print("--- CASO 2 (2 botellas, 1 fruta) ---")
    print(f"Subtotal: ${c2['subtotal']:,}")
    print(f"Descuento: ${c2['descuento']:,}")
    print(f"Total a pagar: ${c2['total_pagar']:,}")
'''
    # Bloque de código formateado
    code_tbl = doc.add_table(rows=1, cols=1)
    code_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    code_tbl.autofit = False
    code_tbl.columns[0].width = Inches(6.5)
    c_code = code_tbl.cell(0, 0)
    set_cell_background(c_code, "282C34") # Fondo oscuro tipo editor
    set_cell_margins(c_code, top=140, bottom=140, left=180, right=180)
    p_code = c_code.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.05
    run_code = p_code.add_run(python_code)
    run_code.font.name = 'Consolas'
    run_code.font.size = Pt(8.5)
    run_code.font.color.rgb = RGBColor(0xE6, 0xEE, 0xF8)

    # Guardar documento
    output_path = r"C:\Users\Coder\.gemini\antigravity\scratch\ejercicio_pausa_activa\Solucion_Compra_Pausa_Activa.docx"
    doc.save(output_path)
    print(f"Documento generado exitosamente en: {output_path}")

if __name__ == "__main__":
    main()
