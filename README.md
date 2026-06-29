<div align="center">

# ⚡ Simulador de Aproximaciones BJT
### *Modelo Ideal vs. Segunda Aproximación — Herramienta Interactiva de Análisis*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2%2B-1F6AA5?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge)](LICENSE)
[![UNMSM](https://img.shields.io/badge/FISI-UNMSM-C00000?style=for-the-badge)](https://www.unmsm.edu.pe/)
[![Status](https://img.shields.io/badge/Estado-En%20Desarrollo-brightgreen?style=for-the-badge)]()

**Aplicación de escritorio moderna y modular para analizar el comportamiento del transistor BJT bajo dos modelos de aproximación de silicio — desarrollada en Python con CustomTkinter.**

</div>

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Los Dos Modelos de Aproximación](#-los-dos-modelos-de-aproximación)
3. [Características Principales](#-características-principales)
4. [Arquitectura Modular](#-arquitectura-modular)
5. [Estructura del Repositorio](#-estructura-del-repositorio)
6. [Requisitos del Sistema](#-requisitos-del-sistema)
7. [Guía de Instalación](#-guía-de-instalación)
8. [Capturas de Pantalla](#-capturas-de-pantalla)
9. [Equipo y Créditos](#-equipo-y-créditos)

---

## 🔬 Descripción General

El **Simulador de Aproximaciones BJT** es una herramienta de escritorio interactiva desarrollada como proyecto académico en la *Universidad Nacional Mayor de San Marcos (FISI-UNMSM)*. Permite a estudiantes de electrónica e ingenieros analizar y comparar el comportamiento eléctrico de un **transistor BJT NPN** en un **circuito de polarización fija**, bajo dos enfoques clásicos de modelado del silicio.

Dados los parámetros del circuito — tensión de alimentación (Vcc), resistencia de base (Rb), resistencia de colector (Rc) y ganancia de corriente (β) — el simulador calcula y visualiza:

- Corriente de base (I_B), corriente de colector (I_C) y tensión colector-emisor (V_CE) para **ambos modelos de forma simultánea**.
- La **región de operación** del transistor: Activa, Saturación o Corte.
- Una **alerta de saturación** cuando V_CE cae por debajo del umbral de 0.2 V.
- El **porcentaje de error analítico** entre ambos modelos, cuantificando el impacto práctico de la suposición sobre Vbe.
- Un **canvas interactivo en tiempo real** con el esquema del circuito y etiquetas actualizadas dinámicamente.
- Una **tabla comparativa lado a lado** para lectura rápida de datos y control de calidad.

> **Objetivo educativo:** Hacer tangible la diferencia que introduce la suposición Vbe = 0 V (Ideal) frente al más realista Vbe = 0.7 V (Segunda Aproximación), y desarrollar intuición sobre cuándo cada modelo es suficientemente preciso.

---

## 📐 Los Dos Modelos de Aproximación

Comprender cómo modelamos el BJT de silicio es el eje central de este simulador. Ambos modelos asumen que el transistor opera en la **región activa** (V_CE > 0.2 V).

### Modelo 1 — Aproximación Ideal (Vbe = 0 V)

En el modelo ideal, la **tensión de la unión Base-Emisor se asume igual a cero**, simplificando el circuito a una red puramente resistiva.

| Parámetro | Fórmula |
|-----------|---------|
| V_BE | 0 V |
| I_B | V_CC / R_B |
| I_C | β × I_B |
| V_CE | V_CC − I_C × R_C |

> ✅ **Recomendado cuando:** V_CC >> 0.7 V (típicamente V_CC ≥ 10 V), haciendo despreciable la caída de Vbe.
> ❌ **Limitación:** Sobreestima las corrientes de base y colector, introduciendo error en circuitos de baja tensión.

---

### Modelo 2 — Segunda Aproximación (Vbe = 0.7 V)

En este modelo, la **unión Base-Emisor se modela como una caída de tensión fija de 0.7 V**, que representa el umbral típico de polarización directa de una unión PN de silicio.

| Parámetro | Fórmula |
|-----------|---------|
| V_BE | 0.7 V |
| I_B | (V_CC − 0.7) / R_B |
| I_C | β × I_B |
| V_CE | V_CC − I_C × R_C |

> ✅ **Recomendado cuando:** Se requiere alta precisión independientemente de la magnitud de V_CC.
> ✅ **Estándar de la industria** para cálculos manuales y diseño inicial de circuitos.

---

### Error Analítico

El simulador calcula el porcentaje de error introducido al usar el Modelo Ideal frente a la Segunda Aproximación:

```
% Error (Ic) = |( Ic_ideal − Ic_2da ) / Ic_2da| × 100
```

Este valor crece significativamente conforme V_CC se acerca a 0.7 V, evidenciando cuándo la suposición ideal se vuelve inaceptable.

---

## ✨ Características Principales

| Característica | Descripción |
|----------------|-------------|
| 🎚️ **Control de Parámetros en Vivo** | Sliders para Vcc, Rb, Rc y β actualizan todos los resultados en tiempo real |
| ⚡ **Cálculo Dual de Modelos** | Modelo Ideal y 2ª Aproximación calculados de forma simultánea |
| 🔴 **Detección de Saturación** | Alerta automática cuando V_CE ≤ 0.2 V (transistor sale de la región activa) |
| 📊 **Tabla Comparativa** | Tabla lado a lado con valores codificados por color y porcentaje de error |
| 🖼️ **Canvas Interactivo** | Esquema del circuito en vivo con etiquetas de tensión y corriente actualizadas dinámicamente |
| 🌙 **Interfaz en Modo Oscuro** | Tema oscuro completo vía CustomTkinter con paleta azul marino y dorado |
| 🧩 **Código Modular** | Cuatro módulos independientes que permiten desarrollo paralelo sin conflictos de fusión |
| 🐍 **Python Puro** | Sin motores de simulación externos — toda la matemática implementada desde cero |

---

## 🏗️ Arquitectura Modular

El proyecto se estructura en **cuatro módulos independientes y débilmente acoplados**, diseñados para permitir el desarrollo paralelo por parte de los integrantes del equipo sin conflictos de fusión (*merge conflicts*). Cada módulo expone una interfaz pública limpia consumida por `main.py`.

```
┌─────────────────────────────────────────────────────────────────┐
│                          main.py                                │
│              (Orquestador — Integrante 3)                       │
│                                                                 │
│  on_slider_change() ──→ get_datos() ──→ calcular() ──→ update() │
└───────┬───────────────────────┬──────────────┬──────────────────┘
        │                       │              │
        ▼                       ▼              ▼
┌───────────────┐   ┌───────────────────┐   ┌─────────────────────┐
│ui_arquitectura│   │  motor_calculo    │   │  analisis_output    │
│  (Int. 1)     │   │    (Int. 2)       │   │    (Int. 4)         │
│               │   │                   │   │                     │
│ • CTkSliders  │   │ • Modelo Ideal    │   │ • Tabla comparativa │
│ • CTkEntries  │   │ • 2ª Aprox.       │   │ • Visualiz. % error │
│ • Maquetación │   │ • Detec. satur.   │   │ • Control calidad   │
│               │   │ • Cálculo error   │   │ • Formato de datos  │
└───────────────┘   └───────────────────┘   └─────────────────────┘
                                                        │
                              ┌─────────────────────────┘
                              ▼
                   ┌─────────────────────┐
                   │   visual_canvas     │
                   │     (Int. 3)        │
                   │                     │
                   │ • Esquema circuito  │
                   │ • Etiquetas dinám.  │
                   │ • Dibujo Tk Canvas  │
                   └─────────────────────┘
```

### Descripción de los Módulos

#### `ui_arquitectura.py` — Integrante 1 · *Capa de Interfaz*
Responsable del **panel de entrada completo**: sliders de CustomTkinter (Vcc, Rb, Rc, Beta), campos de entrada numérica con validación, etiquetas de unidades (V, kΩ), botones de reinicio y el layout general de la ventana. Expone `PanelParametros`, una subclase de `CTkFrame` con un método `get_datos() → dict` y un hook `set_callback(fn)` que se invoca en cada interacción con los sliders.

#### `motor_calculo.py` — Integrante 2 · *Motor de Cálculo*
El **núcleo matemático puro** de la aplicación. No contiene código de interfaz gráfica. Implementa `calcular(datos_circuito: dict) → dict`, que aplica ambos modelos BJT, evalúa la región de operación (Activa / Saturación / Corte), activa una bandera de alerta de saturación cuando V_CE ≤ 0.2 V y calcula el porcentaje de error analítico. Todas las fórmulas se derivan de *Electronic Devices and Circuit Theory* de Boylestad.

#### `visual_canvas.py` — Integrante 3 · *Esquema del Circuito*
Un `CTkFrame` que contiene un **Canvas estándar de Tkinter** que dibuja el esquema BJT de polarización fija desde cero usando primitivas nativas (`create_line`, `create_rectangle`, `create_text`, `create_oval`). No se requieren archivos de imagen externos. Expone `actualizar_valores(resultados: dict)`, que actualiza en tiempo real todas las etiquetas de valores flotantes sobre el esquema.

#### `analisis_output.py` — Integrante 4 · *Salida y Control de Calidad*
Renderiza la **tabla comparativa lado a lado** entre ambos modelos usando `CTkFrame` y layout de grilla. Muestra Vbe, Ib, Ic, Vce, región de operación y el porcentaje de error analítico con indicadores codificados por color. Expone `TablaResultados`, una subclase de `CTkFrame` con un método `actualizar(resultados: dict)`.

#### `main.py` — Integrante 3 · *Orquestador*
El **punto de entrada ejecutable**. Inicializa la ventana raíz `customtkinter.CTk`, instancia los cuatro módulos y los conecta a través del manejador de eventos central `_on_parametros_cambiados()`. Incluye clases `_MockXxx` de respaldo para cada módulo, permitiendo que cualquier integrante ejecute la aplicación completa de forma independiente mientras los demás módulos aún están en desarrollo.

---

## 📁 Estructura del Repositorio

```
bjt-approximation-simulator/
│
├── 📄 main.py                  # Punto de entrada y orquestador (Integrante 3)
├── 🖼️  visual_canvas.py         # Canvas interactivo del circuito (Integrante 3)
│
├── 🎚️  ui_arquitectura.py       # Panel de parámetros y maquetación (Integrante 1)
├── ⚙️  motor_calculo.py         # Motor matemático BJT (Integrante 2)
├── 📊 analisis_output.py        # Tabla comparativa y control de calidad (Integrante 4)
│
├── 📋 requirements.txt          # Dependencias de Python
├── 📖 README.md                 # Este archivo
└── 📜 LICENSE                   # Licencia MIT
```

> **Nota:** El proyecto no utiliza archivos de recursos externos (sin imágenes, sin fuentes, sin configuraciones JSON). Todo se renderiza programáticamente, haciendo el repositorio completamente portable y listo para ejecutar tras clonar.

---

## 💻 Requisitos del Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **Sistema Operativo** | Windows 10, macOS 11, Ubuntu 20.04 | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Versión de Python** | 3.10 | 3.11 o 3.12 |
| **Memoria RAM** | 256 MB libres | 512 MB libres |
| **Resolución de Pantalla** | 1280 × 720 | 1920 × 1080 |
| **Conexión a Internet** | Requerida (solo primera instalación) | — |

**Paquetes requeridos** (instalados vía `requirements.txt`):

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `customtkinter` | ≥ 5.2.2 | Widgets modernos de GUI y sistema de temas |
| `Pillow` | ≥ 10.0.0 | Renderizado de imágenes dentro de widgets CTkImage |
| `tkinter` | stdlib | Dibujo en Canvas (incluido con Python) |

---

## 🚀 Guía de Instalación

Sigue estos pasos para poner en marcha el simulador en tu equipo.

### Paso 1 — Clonar el Repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/<tu-usuario>/bjt-approximation-simulator.git
cd bjt-approximation-simulator
```

### Paso 2 — Crear un Entorno Virtual *(Recomendado)*

Usar un entorno virtual mantiene limpio el Python del sistema.

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio del prompt de tu terminal.

### Paso 3 — Instalar las Dependencias

```bash
pip install -r requirements.txt
```

Salida esperada:
```
Successfully installed customtkinter-5.2.2 Pillow-10.x.x darkdetect-x.x.x
```

> **Usuarios de Linux:** Si aparece el error `_tkinter`, instala primero el paquete del sistema:
> ```bash
> sudo apt-get install python3-tk   # Debian/Ubuntu
> sudo dnf install python3-tkinter  # Fedora
> ```

### Paso 4 — Ejecutar la Aplicación

```bash
python main.py
```

La ventana del simulador se abrirá de inmediato. Todos los módulos se cargan automáticamente; si el archivo de algún integrante aún no existe, los respaldos Mock internos se activan silenciosamente.

### Solución de Problemas

| Error | Causa Probable | Solución |
|-------|---------------|----------|
| `ModuleNotFoundError: customtkinter` | Dependencias no instaladas | Ejecutar nuevamente `pip install -r requirements.txt` |
| `No module named '_tkinter'` | tkinter no incluido en Python | Instalar `python3-tk` (Linux) o reinstalar Python (Windows/macOS) |
| Ventana demasiado pequeña | Pantalla de baja resolución o DPI | Redimensionar manualmente o ajustar `window.geometry("1200x700")` en `main.py` |
| `ImportError: cannot import name 'CTkFont'` | Versión de CustomTkinter desactualizada | Ejecutar `pip install --upgrade customtkinter` |

---

## 📸 Capturas de Pantalla

> *Las siguientes capturas se añadirán al completar la interfaz final.*

### Ventana Principal de la Aplicación

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   [ Captura: Ventana completa de la aplicación — modo oscuro ]          ║
║   Muestra el layout de tres columnas: Panel de Parámetros |             ║
║   Canvas del Circuito | Tabla Comparativa. Sliders en valores           ║
║   por defecto.                                                           ║
║                                                                          ║
║   📌 Ruta: docs/capturas/ventana_principal.png                           ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Canvas Interactivo del Circuito

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   [ Captura: Módulo visual_canvas ]                                      ║
║   Esquema BJT de polarización fija con etiquetas en vivo de             ║
║   Vbe / Ib / Ic / Vce. Columna izquierda: valores Ideal (azul).         ║
║   Columna derecha: 2ª Aproximación (naranja).                            ║
║                                                                          ║
║   📌 Ruta: docs/capturas/canvas_circuito.png                             ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Alerta de Saturación

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   [ Captura: Alerta de detección de saturación ]                        ║
║   Indicador rojo visible cuando Vce ≤ 0.2 V.                            ║
║   Barra de estado: "⚠ SATURACIÓN — Vce por debajo del umbral 0.2 V"    ║
║                                                                          ║
║   📌 Ruta: docs/capturas/alerta_saturacion.png                           ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Tabla Comparativa y Análisis de Error

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   [ Captura: Módulo analisis_output — tabla comparativa ]               ║
║   Parámetros: Vcc=5V, Rb=100kΩ, Rc=1kΩ, β=150                          ║
║   Error analítico Ic ≈ 16.3% — error elevado a baja tensión de Vcc.     ║
║                                                                          ║
║   📌 Ruta: docs/capturas/tabla_comparativa.png                           ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 👥 Equipo y Créditos

Este proyecto fue desarrollado como parte del currículo académico en:

> **Universidad Nacional Mayor de San Marcos**
> Facultad de Ingeniería de Sistemas e Informática (FISI)
> Curso: *[Nombre del Curso]* — Prof. Mg. Ing. *[Nombre del Docente]*

---

| Rol | Integrante | Módulo | Responsabilidades |
|-----|-----------|--------|------------------|
| 🎚️ **Desarrollador UI** | Integrante 1 | `ui_arquitectura.py` | Sliders, entradas, maquetación, diseño UX |
| ⚙️ **Motor Matemático** | Integrante 2 | `motor_calculo.py` | Fórmulas BJT, lógica de saturación, cálculo de error |
| 🖼️ **Canvas y Arquitectura** | Integrante 3 | `visual_canvas.py` · `main.py` | Esquema del circuito, orquestación de la app |
| 📊 **Salida y Control de Calidad** | Integrante 4 | `analisis_output.py` | Tabla comparativa, formato de datos, QA |

---

### Referencias Bibliográficas

- Boylestad, R. L., & Nashelsky, L. *Electronic Devices and Circuit Theory*, 11.ª ed. Pearson.
- Sedra, A. S., & Smith, K. C. *Microelectronic Circuits*, 7.ª ed. Oxford University Press.
- Documentación de CustomTkinter: [github.com/TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

<div align="center">

Hecho con ⚡ y Python · FISI-UNMSM · 2025

</div>
