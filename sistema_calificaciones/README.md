# Sistema de Registro y Procesamiento de Calificaciones
**Documentación Técnica de Arquitectura, Dominio y Persistencia**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Architecture: Clean](https://img.shields.io/badge/Architecture-Clean%20Architecture-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Repository](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones)

Repositorio oficial: [https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones](https://github.com/JayzirTech/Sena/tree/main/sistema_calificaciones)

---

## 1. Arquitectura de Software (Clean Architecture)

El sistema implementa los principios de **Clean Architecture**, desacoplando estrictamente las reglas matemáticas y de negocio de la infraestructura de almacenamiento y la interfaz de usuario.

```text
sistema_calificaciones/
│
├── data/
│   ├── estudiantes.csv            # Dimensión Maestro de Aprendices (Soft Delete)
│   └── calificaciones.csv         # Tabla Transaccional de Calificaciones
│
├── src/
│   ├── domain/                    # Capa 1: Entidades y Reglas de Negocio Puras
│   │   ├── models.py              # Data classes (Estudiante, Calificacion, Boletin)
│   │   └── services.py            # Fórmulas de promedios, correos y deduplicación
│   │
│   ├── application/               # Capa 2: Casos de Uso (Puertos y Lógica de Aplicación)
│   │   ├── interfaces.py          # Abstract Base Classes (Repositories)
│   │   └── use_cases.py           # Orquestación transaccional con confirmación
│   │
│   ├── infrastructure/            # Capa 3: Persistencia y Adaptadores Externos
│   │   └── repositories.py        # Implementación atómica sobre archivos CSV
│   │
│   └── presentation/              # Capa 4: Interfaz de Consola Interactiva (CLI)
│       ├── console.py             # Renderizado visual, tablas y cls
│       └── controller.py          # Controladores de menús, submenús y confirmación S/N
│
├── scripts/
│   └── prueba_escritorio.py       # Prueba de escritorio algorítmica
├── tests/
│   └── test_sistema.py            # Suite de pruebas unitarias (unittest)
├── DOCUMENTACION.md               # Manual de usuario (Lenguaje no técnico)
├── DOCUMENTACION.pdf              # Documentación oficial compilada en PDF
├── seed.py                        # Script de inyección de datos de prueba
├── main.py                        # Bootstrap y Composition Root
└── README.md                      # Esta especificación técnica
```

---

## 2. Modelo de Datos y Persistencia Relacional Ligera

El sistema almacena la información en dos archivos planos con formato **CSV**, aplicando normalización relacional:

### 2.1. Maestro de Estudiantes: `data/estudiantes.csv`
Implementa clave primaria secuencial y **Borrado Lógico (*Soft Delete*)**:

| Campo | Tipo | Clave | Restricciones / Reglas |
| :--- | :--- | :--- | :--- |
| `id_estudiante` | `VARCHAR(10)` | **PK** | Formato secuencial de 4 dígitos: `EST-0001` a `EST-9999` |
| `documento` | `VARCHAR(20)` | **UNIQUE** | Documento legal único (CC / TI) |
| `nombre_completo`| `VARCHAR(100)`| | Nombre completo normalizado |
| `correo` | `VARCHAR(100)`| **UNIQUE** | Formato: `nombre.apellido@sena.edu.co` con sufijo anti-colisión |
| `estado` | `VARCHAR(10)` | | `ACTIVO` o `INACTIVO` (Preserva histórico) |

### 2.2. Tabla de Hechos: `data/calificaciones.csv`
Almacena transacciones individuales sin límite de notas por estudiante ni materia:

| Campo | Tipo | Clave | Restricciones / Reglas |
| :--- | :--- | :--- | :--- |
| `id_calificacion`| `INT` | **PK** | Secuencial único autoincremental |
| `id_estudiante` | `VARCHAR(10)` | **FK** | Referencia a `estudiantes.csv` |
| `id_materia` | `VARCHAR(10)` | **FK** | `MAT`, `LIT`, `SOC`, `QUI`, `PROG` |
| `periodo` | `INT` | | Valor entero del 1 al 4 |
| `nota` | `FLOAT` | | Rango $0.0 \le \text{nota} \le 100.0$ |
| `fecha` | `DATE` | | Marca de tiempo ISO `YYYY-MM-DD` |

---

## 3. Modelo Matemático y Lógica de Negocio

### 3.1. Promedio por Periodo
Para un estudiante $e$, materia $m$ y periodo $p$ con $k$ notas:
$$\bar{x}_{e, m, p} = \frac{\sum_{i=1}^{k} \text{nota}_{i}}{k}$$

### 3.2. Definitiva Anual por Asignatura
La definitiva se calcula dividiendo **estrictamente entre los 4 periodos** (los periodos sin notas computan como $0.0$):
$$\text{Definitiva}_{e, m} = \frac{\sum_{p=1}^{4} \bar{x}_{e, m, p}}{4.0}$$

### 3.3. Promedio General del Año Escolar
Media aritmética estricta de las 5 asignaturas:
$$\bar{X}_{e, \text{año}} = \frac{\sum_{m=1}^{5} \text{Definitiva}_{e, m}}{5.0}$$

### 3.4. Condición de Promoción
$$\text{Estado}(e) = \begin{cases} \text{APROBADO}, & \text{si } \bar{X}_{e, \text{año}} \ge 70.0 \\ \text{NO APROBADO}, & \text{si } \bar{X}_{e, \text{año}} < 70.0 \end{cases}$$

---

## 4. Comandos de Ejecución

### 4.1. Iniciar el Portal Interactivo
```bash
python main.py
```

### 4.2. Inyectar Datos de Prueba (Seeder)
Para poblar automáticamente la base de datos con estudiantes y notas de ejemplo:
```bash
python seed.py
# O alternativamente:
python main.py --seed
```

### 4.3. Ejecutar Pruebas Unitarias
```bash
python -m unittest discover tests
```

### 4.4. Ejecutar Prueba de Escritorio Algorítmica
```bash
python scripts/prueba_escritorio.py
```
