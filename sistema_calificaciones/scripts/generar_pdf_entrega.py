"""
Compilador a PDF para el documento formal de entrega de la evidencia SENA.
Genera ENTREGA_EVIDENCIA_SENA.pdf con formato académico institucional.
"""
import os
import subprocess

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Evidencia de Aprendizaje - Sistema de Calificaciones SENA</title>
    <style>
        @page {
            size: letter;
            margin: 2.2cm 2cm;
            @bottom-right {
                content: "Página " counter(page);
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            color: #24292f;
            line-height: 1.5;
            font-size: 10.5pt;
        }
        .header-sena {
            border-bottom: 3px solid #39a900;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        .header-sena h1 {
            color: #04324f;
            font-size: 18pt;
            margin: 0;
            text-transform: uppercase;
        }
        .header-sena .sub {
            color: #57606a;
            font-size: 11pt;
            margin-top: 4px;
        }
        .meta-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
            font-size: 9.5pt;
        }
        .meta-table th, .meta-table td {
            border: 1px solid #d0d7de;
            padding: 8px 12px;
            text-align: left;
        }
        .meta-table th {
            background-color: #f6f8fa;
            color: #04324f;
            width: 25%;
        }
        h2 {
            color: #04324f;
            border-bottom: 1.5px solid #d0d7de;
            padding-bottom: 4px;
            margin-top: 22px;
            font-size: 13pt;
        }
        h3 {
            color: #39a900;
            font-size: 11pt;
            margin-top: 14px;
        }
        p, li {
            font-size: 10pt;
            text-align: justify;
        }
        .card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #39a900;
            padding: 10px 14px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 9.5pt;
        }
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 8.5pt;
        }
        table.data-table th, table.data-table td {
            border: 1px solid #cbd5e1;
            padding: 6px 8px;
            text-align: center;
        }
        table.data-table th {
            background-color: #04324f;
            color: white;
            font-weight: 600;
        }
        table.data-table tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .badge-pass {
            background-color: #dcfce7;
            color: #15803d;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .badge-fail {
            background-color: #fee2e2;
            color: #b91c1c;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
        }
        pre {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 5px;
            padding: 10px;
            font-size: 8pt;
            font-family: Consolas, "Courier New", monospace;
            overflow-x: auto;
            line-height: 1.35;
        }
        .footer {
            margin-top: 35px;
            border-top: 1px solid #e2e8f0;
            padding-top: 10px;
            font-size: 8.5pt;
            color: #64748b;
            text-align: center;
        }
        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>

    <div class="header-sena">
        <h1>Evidencia de Aprendizaje</h1>
        <div class="sub">Sistema de Registro y Procesamiento de Calificaciones &bull; Formación Tecnológica SENA</div>
    </div>

    <table class="meta-table">
        <tr>
            <th>Reto Principal:</th>
            <td>Sistema de registro y procesamiento de calificaciones</td>
        </tr>
        <tr>
            <th>Aprendiz:</th>
            <td><strong>Jayzir Martinez</strong> (Modalidad Individual)</td>
        </tr>
        <tr>
            <th>Repositorio GitHub:</th>
            <td><a href="https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones">https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones</a></td>
        </tr>
        <tr>
            <th>Tecnologías:</th>
            <td>Algoritmia, Pseudocódigo (PSeInt), Python 3.12 (Clean Architecture), Persistencia CSV</td>
        </tr>
        <tr>
            <th>Fecha:</th>
            <td>17 de noviembre de 2026</td>
        </tr>
    </table>

    <h2>1. Comprensión de la Situación Problema</h2>
    <p>
        Una institución educativa requiere un algoritmo y sistema computacional capaz de registrar las calificaciones de múltiples aprendices en un salón de clases, calcular sus promedios parciales y definitivos, evaluar automáticamente su condición de aprobación con un umbral mínimo de <strong>70 puntos</strong> (&ge; 70.0) y, al finalizar el procesamiento, generar el consolidado y <strong>promedio general del grupo</strong>.
    </p>

    <h2>2. Descomposición del Problema (E-P-S)</h2>
    <ul>
        <li><strong>Entradas:</strong> Documento del aprendiz, nombre completo, asignatura (Matemáticas, Literatura, Ciencias Sociales, Química, Programación), periodo lectivo (1 a 4) y calificaciones numéricas (0 a 100).</li>
        <li><strong>Procesos:</strong> Cálculo de promedio por periodo, cálculo de definitiva anual dividiendo estrictamente entre 4 periodos, promedio general del aprendiz, evaluación condicional (&ge; 70) y acumulación global del grupo.</li>
        <li><strong>Salidas:</strong> Estado individual (Aprobado / No Aprobado), boletín académico detallado, resumen por materia y promedio general del salón.</li>
    </ul>

    <h2>3. Definición de Variables y Estructuras</h2>
    <div class="card">
        <strong>Variables de Control y Datos:</strong> <code>id_estudiante</code> (Texto, autogenerado), <code>documento</code> (Texto), <code>nombre_completo</code> (Texto), <code>correo</code> (Texto institucional), <code>estado</code> (Texto, borrado lógico).<br>
        <strong>Variables Matemáticas y Acumuladores:</strong> <code>nota</code> (Real), <code>promPeriodo</code> (Real), <code>definitivaMateria</code> (Real), <code>promedioGeneral</code> (Real), <code>sumaPromediosSalon</code> (Acumulador Real), <code>totalAprendices</code> (Contador Entero).<br>
        <strong>Estructuras / Arreglos:</strong> Vectores de calificaciones dinámicas sin límite, matrices de resumen anual por periodo y persistencia relacional en archivos <code>data/estudiantes.csv</code> y <code>data/calificaciones.csv</code>.
    </div>

    <div class="page-break"></div>

    <h2>4. Algoritmo en Pseudocódigo (Estándar SENA / PSeInt)</h2>
<pre>
Algoritmo SistemaRegistroCalificaciones
    Definir numAprendices, i, j, cantNotas Como Entero
    Definir nombre, estado Como Cadena
    Definir nota, sumaNotas, definitivaMateria, sumaDefinitivas, promAprendiz Como Real
    Definir sumaPromediosGrupo, promedioGeneralGrupo Como Real

    sumaPromediosGrupo &lt;- 0.0

    Escribir "Ingrese cantidad de aprendices en el grupo: "
    Leer numAprendices

    Para i &lt;- 1 Hasta numAprendices Con Paso 1 Hacer
        Escribir "------------------------------------------------------"
        Escribir "APRENDIZ #", i, ": Ingrese nombre:"
        Leer nombre
        sumaDefinitivas &lt;- 0.0

        Para j &lt;- 1 Hasta 5 Con Paso 1 Hacer // 5 Asignaturas
            Escribir "Asignatura ", j, " - Ingrese total de notas en el año:"
            Leer cantNotas
            sumaNotas &lt;- 0.0
            Para k &lt;- 1 Hasta cantNotas Con Paso 1 Hacer
                Leer nota
                sumaNotas &lt;- sumaNotas + nota
            FinPara
            Si cantNotas &gt; 0 Entonces
                definitivaMateria &lt;- sumaNotas / cantNotas
            Sino
                definitivaMateria &lt;- 0.0
            FinSi
            sumaDefinitivas &lt;- sumaDefinitivas + definitivaMateria
        FinPara

        promAprendiz &lt;- sumaDefinitivas / 5.0

        // Estructura de Decisión: Aprobación >= 70.0
        Si promAprendiz &gt;= 70.0 Entonces
            estado &lt;- "APROBADO"
        Sino
            estado &lt;- "NO APROBADO"
        FinSi

        Escribir "Resultado: ", nombre, " | Promedio: ", promAprendiz, " | Estado: ", estado
        sumaPromediosGrupo &lt;- sumaPromediosGrupo + promAprendiz
    FinPara

    Si numAprendices &gt; 0 Entonces
        promedioGeneralGrupo &lt;- sumaPromediosGrupo / numAprendices
    Sino
        promedioGeneralGrupo &lt;- 0.0
    FinSi

    Escribir "=========================================================="
    Escribir "PROMEDIO GENERAL DEL GRUPO: ", promedioGeneralGrupo
    Escribir "=========================================================="
FinAlgoritmo
</pre>

    <h2>5. Prueba de Escritorio (Desk Check)</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th>#</th>
                <th>Aprendiz</th>
                <th>ID</th>
                <th>Matemáticas</th>
                <th>Programación</th>
                <th>Literatura</th>
                <th>Sociales</th>
                <th>Química</th>
                <th>Promedio Final</th>
                <th>Condición (&ge; 70)</th>
                <th>Estado</th>
                <th>Acumulado Salón</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Ana María Gómez</td>
                <td>EST-0001</td>
                <td>85.0</td>
                <td>95.0</td>
                <td>80.0</td>
                <td>78.0</td>
                <td>72.0</td>
                <td><strong>82.00</strong></td>
                <td>82.00 &ge; 70.0 (V)</td>
                <td><span class="badge-pass">APROBADO</span></td>
                <td>82.00</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Carlos Ramírez</td>
                <td>EST-0002</td>
                <td>62.5</td>
                <td>77.5</td>
                <td>70.0</td>
                <td>68.0</td>
                <td>58.5</td>
                <td><strong>67.30</strong></td>
                <td>67.30 &ge; 70.0 (F)</td>
                <td><span class="badge-fail">NO APROBADO</span></td>
                <td>149.30</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Laura Restrepo</td>
                <td>EST-0003</td>
                <td>93.5</td>
                <td>99.0</td>
                <td>90.0</td>
                <td>92.0</td>
                <td>88.0</td>
                <td><strong>92.50</strong></td>
                <td>92.50 &ge; 70.0 (V)</td>
                <td><span class="badge-pass">APROBADO</span></td>
                <td>241.80</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Juan Morales</td>
                <td>EST-0004</td>
                <td>75.0</td>
                <td>82.0</td>
                <td>85.0</td>
                <td>80.0</td>
                <td>76.0</td>
                <td><strong>79.60</strong></td>
                <td>79.60 &ge; 70.0 (V)</td>
                <td><span class="badge-pass">APROBADO</span></td>
                <td>321.40</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Sofía Herrera</td>
                <td>EST-0005</td>
                <td>50.0</td>
                <td>65.0</td>
                <td>62.0</td>
                <td>60.0</td>
                <td>58.0</td>
                <td><strong>59.00</strong></td>
                <td>59.00 &ge; 70.0 (F)</td>
                <td><span class="badge-fail">NO APROBADO</span></td>
                <td>380.40</td>
            </tr>
        </tbody>
    </table>

    <div class="card">
        <strong>Resultados del Salón:</strong><br>
        &bull; Total Aprendices Evaluados: 5<br>
        &bull; <strong>Promedio General del Salón:</strong> 380.40 / 5 = <strong>76.08</strong><br>
        &bull; Tasa de Aprobación: 3 Aprobados (60.0%) | 2 No Aprobados (40.0%)<br>
        &bull; Aprendiz Destacado: Laura Restrepo (Promedio: 92.50)
    </div>

    <h2>6. Implementación y Código Fuente en GitHub</h2>
    <p>
        El proyecto completo se encuentra alojado y versionado en el repositorio oficial de GitHub:
    </p>
    <div class="card">
        👉 <strong>URL del Repositorio:</strong> 
        <a href="https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones">https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones</a>
    </div>

    <div class="footer">
        Servicio Nacional de Aprendizaje (SENA) &bull; Jayzir Martinez &bull; Noviembre 2026
    </div>

</body>
</html>
"""


def compilar_pdf_entrega():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_path = os.path.join(base_dir, "ENTREGA_EVIDENCIA_TEMP.html")
    pdf_path = os.path.join(base_dir, "ENTREGA_EVIDENCIA_SENA.pdf")

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

    print(f">> Generando PDF de Entrega: {pdf_path}")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(html_path):
        os.remove(html_path)

    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f">> ¡PDF de Entrega generado con éxito! ({os.path.getsize(pdf_path)} bytes)")
        return True
    else:
        print(" [!] Error al compilar PDF:", res.stderr)
        return False


if __name__ == "__main__":
    compilar_pdf_entrega()
