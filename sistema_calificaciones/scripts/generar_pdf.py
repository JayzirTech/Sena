"""
Script para compilar la Documentación a PDF usando Microsoft Edge Headless.
Genera el archivo DOCUMENTACION.pdf con estilo editorial limpio y profesional.
"""
import os
import subprocess
import sys

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Manual de Usuario - Sistema de Calificaciones SENA</title>
    <style>
        @page {
            size: letter;
            margin: 2.2cm 2cm;
            @bottom-right {
                content: counter(page);
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #24292f;
            line-height: 1.6;
            font-size: 11pt;
            margin: 0;
            padding: 0;
        }
        h1 {
            color: #04324f;
            border-bottom: 3px solid #39a900;
            padding-bottom: 8px;
            font-size: 22pt;
            margin-top: 0;
        }
        h2 {
            color: #04324f;
            border-bottom: 1px solid #d0d7de;
            padding-bottom: 6px;
            margin-top: 24px;
            font-size: 15pt;
        }
        h3 {
            color: #39a900;
            font-size: 12pt;
            margin-top: 18px;
        }
        .subtitle {
            font-size: 13pt;
            color: #57606a;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        .repo-badge {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-left: 5px solid #39a900;
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 25px;
            font-size: 10.5pt;
        }
        .repo-badge a {
            color: #0969da;
            text-decoration: none;
            font-weight: bold;
        }
        .rule-card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px 18px;
            margin-bottom: 12px;
        }
        .rule-card strong {
            color: #04324f;
        }
        ul, ol {
            padding-left: 22px;
        }
        li {
            margin-bottom: 6px;
        }
        .alert-box {
            background-color: #e6fffa;
            border: 1px solid #b2f5ea;
            border-left: 5px solid #319795;
            padding: 10px 14px;
            border-radius: 4px;
            margin: 15px 0;
        }
        .footer {
            margin-top: 40px;
            border-top: 1px solid #eaeaea;
            padding-top: 10px;
            font-size: 9pt;
            color: #8c8c8c;
            text-align: center;
        }
    </style>
</head>
<body>

    <h1>Manual de Usuario: Sistema de Calificaciones</h1>
    <div class="subtitle">Guía de Uso para Docentes, Coordinadores y Aprendices &bull; Salón Único</div>

    <div class="repo-badge">
        <strong>Repositorio Oficial del Proyecto:</strong><br>
        <a href="https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones">
            https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones
        </a>
    </div>

    <h2>1. ¿Qué es este sistema?</h2>
    <p>
        Este sistema es una herramienta diseñada para facilitar la labor de los docentes y directivos en el registro y procesamiento de notas de un salón de clases.
    </p>
    <p>
        Permite llevar el control completo de los estudiantes, calcular sus promedios de manera automática y saber al instante si un estudiante aprueba o reprueba el año escolar, sin necesidad de realizar cálculos manuales ni recurrir a complejas hojas de cálculo.
    </p>

    <h2>2. ¿Cómo funciona el año escolar?</h2>
    <div class="rule-card">
        <strong>1. Las 5 Materias del Salón:</strong>
        Todos los aprendices cursan exactamente 5 asignaturas: Matemáticas, Literatura, Ciencias Sociales, Química y Programación de Software.
    </div>

    <div class="rule-card">
        <strong>2. Los 4 Periodos Académicos:</strong>
        El año lectivo está dividido en 4 periodos. El sistema mantiene los periodos siempre abiertos y disponibles para ingresar, consultar o corregir notas en cualquier momento.
    </div>

    <div class="rule-card">
        <strong>3. Cálculo de la Nota Definitiva de Cada Materia:</strong>
        En cada periodo se pueden ingresar todas las notas que se deseen. El sistema calcula el promedio de cada periodo. La definitiva anual de la materia se obtiene sumando los promedios de los 4 periodos y dividiendo siempre estrictamente entre 4.
    </div>

    <div class="rule-card">
        <strong>4. Criterio de Aprobación del Año Escolar:</strong>
        El estudiante aprueba el año escolar si el promedio general de todas sus materias es <strong>igual o superior a 70 puntos</strong>.
    </div>

    <div class="rule-card">
        <strong>5. Recuperaciones y Nivelaciones:</strong>
        Toda nota de examen o taller de recuperación se asienta como una calificación adicional dentro del periodo respectivo, sumando directamente a su promedio para ayudar al aprendiz.
    </div>

    <h2>3. Guía Paso a Paso: ¿Cómo usar el sistema?</h2>

    <div class="alert-box">
        <strong>Regla de oro de navegación:</strong> Para salir del sistema o regresar al menú anterior en cualquier momento, simplemente presione el número <strong>0</strong>.
    </div>

    <h3>Paso 1: Registrar un nuevo aprendiz</h3>
    <p>
        En el menú principal, elija la opción <strong>[1]</strong>. Ingrese el número de documento de identidad y el nombre completo. El sistema generará automáticamente un código ordenado (como <em>EST-0001</em>) y su correo institucional (ejemplo: <em>ana.gomez@sena.edu.co</em>). Tras su confirmación, los datos quedan guardados y listos.
    </p>

    <h3>Paso 2: Dar de baja a un estudiante que se retira</h3>
    <p>
        Elija la opción <strong>[2]</strong>. El sistema aplica un borrado lógico: oculta al estudiante para que no vuelva a aparecer en las listas activas, pero <em>jamás borra su historial ni sus notas anteriores</em> de la base de datos, garantizando la auditoría histórica.
    </p>

    <h3>Paso 3: Calificar a un estudiante</h3>
    <p>
        En la opción <strong>[3]</strong>, seleccione al aprendiz de la lista (o busque por nombre/cédula), elija la materia, el periodo (1 a 4) y digite la calificación (entre 0 y 100). El sistema le mostrará un resumen y le pedirá confirmación antes de guardar.
    </p>

    <h3>Paso 4: Corregir o borrar una nota</h3>
    <p>
        Si se cometió un error de digitación, la opción <strong>[4]</strong> le permite seleccionar al aprendiz, listar todas sus calificaciones previas y corregir el valor o eliminar la nota por completo bajo confirmación.
    </p>

    <h3>Paso 5: Consultar Reportes y Boletines</h3>
    <ul>
        <li><strong>Opción [5] - Boletín Individual:</strong> Muestra la sábana de notas del estudiante, promedios por periodo, definitiva anual, materias aprobadas y estado final.</li>
        <li><strong>Opción [6] - Resumen del Salón:</strong> Presenta el consolidado de todo el grupo, el promedio general del salón, tasa de aprobación y el cuadro de honor.</li>
    </ul>

    <h2>4. Seguridad y Confirmación Obligatoria</h2>
    <p>
        Para prevenir errores accidentales, toda acción que guarde, modifique o elimine datos requiere una confirmación explícita (<strong>S/N</strong>) por parte del usuario.
    </p>

    <div class="footer">
        Portal de Calificaciones SENA &bull; Formación Tecnológica &bull; JayzirTech
    </div>

</body>
</html>
"""


def compilar_pdf():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_path = os.path.join(base_dir, "DOCUMENTACION_TEMP.html")
    pdf_path = os.path.join(base_dir, "DOCUMENTACION.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_bin):
        edge_bin = "msedge"

    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    print(f">> Generando PDF: {pdf_path}")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(html_path):
        os.remove(html_path)

    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f">> ¡PDF generado exitosamente! ({os.path.getsize(pdf_path)} bytes)")
        return True
    else:
        print(" [!] Error al compilar PDF:", res.stderr)
        return False


if __name__ == "__main__":
    compilar_pdf()
