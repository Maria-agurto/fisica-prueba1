"""
main.py
=======
Módulo: Integrante 3 — Orquestador Principal
Proyecto: Simulador de Aproximaciones del Transistor BJT
Curso: [Nombre del curso] — FISI-UNMSM

Descripción:
    Punto de entrada del simulador BJT. Inicializa la ventana raíz de
    CustomTkinter e integra todos los módulos del equipo bajo el patrón
    MVC ligero:
        - ui_arquitectura  (Integrante 1): sliders/inputs de parámetros
        - motor_calculo    (Integrante 2): cálculos Ideal / 2ª Aprox.
        - visual_canvas    (Integrante 3): lienzo gráfico del circuito
        - analisis_output  (Integrante 4): tabla comparativa

    MOCKS: Mientras los demás integrantes terminan sus módulos, este archivo
    define versiones simuladas de ui_arquitectura, motor_calculo y
    analisis_output que permiten ejecutar y probar la app de forma inmediata.

Uso:
    python main.py

Dependencias:
    - customtkinter >= 5.2
    - visual_canvas (este proyecto)
"""

from __future__ import annotations

import importlib
import tkinter as tk
from typing import Any, Callable

import customtkinter as ctk

import visual_canvas  # Módulo propio (Integrante 3)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — MÓDULOS MOCK
# ══════════════════════════════════════════════════════════════════════════════
# Cada clase Mock replica la interfaz pública del módulo real.
# Cuando el integrante correspondiente entregue su archivo, basta con
# eliminar la clase Mock y descomentar el import real.
# ══════════════════════════════════════════════════════════════════════════════


class _MockUiArquitectura:
    """
    Mock del módulo ui_arquitectura (Integrante 1).

    Interfaz pública que se espera del módulo real:
        - PanelParametros(master) → CTkFrame con sliders para Vcc, Rb, Rc, Beta
        - panel.set_callback(fn)  → registra la función a llamar al cambiar sliders
        - panel.get_datos()       → dict {"Vcc", "Rb", "Rc", "Beta"}
    """

    class PanelParametros(ctk.CTkFrame):
        """Panel de controles deslizantes para los parámetros del circuito."""

        # Rangos y valores por defecto de cada parámetro
        _PARAMS: dict[str, dict[str, float]] = {
            "Vcc":  {"from": 1.0,   "to": 30.0,   "default": 12.0,  "step": 0.5},
            "Rb":   {"from": 1.0,   "to": 1000.0, "default": 470.0, "step": 1.0},
            "Rc":   {"from": 0.1,   "to": 100.0,  "default": 4.7,   "step": 0.1},
            "Beta": {"from": 10.0,  "to": 500.0,  "default": 100.0, "step": 1.0},
        }

        _UNITS: dict[str, str] = {
            "Vcc":  "V",
            "Rb":   "kΩ",
            "Rc":   "kΩ",
            "Beta": "",
        }

        def __init__(self, master: Any, **kwargs: Any) -> None:
            super().__init__(master, fg_color="#16213e", corner_radius=10, **kwargs)
            self._callback: Callable | None = None
            self._vars: dict[str, ctk.DoubleVar] = {}
            self._value_labels: dict[str, ctk.CTkLabel] = {}
            self._build()

        def _build(self) -> None:
            """Construye los sliders del panel."""
            ctk.CTkLabel(
                self,
                text="⚙  Parámetros del Circuito",
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color="#e2e8f0",
            ).pack(pady=(14, 8), padx=14, anchor="w")

            # Separador
            ctk.CTkFrame(self, height=1, fg_color="#334155").pack(
                fill="x", padx=14, pady=(0, 10)
            )

            for name, cfg in self._PARAMS.items():
                self._build_slider_row(name, cfg)

            # Botón de reset
            ctk.CTkButton(
                self,
                text="↺  Restablecer valores",
                fg_color="#1e293b",
                hover_color="#334155",
                text_color="#94a3b8",
                font=ctk.CTkFont(family="Consolas", size=11),
                command=self._reset_defaults,
                height=30,
                corner_radius=6,
            ).pack(fill="x", padx=14, pady=(6, 14))

        def _build_slider_row(self, name: str, cfg: dict[str, float]) -> None:
            """Crea una fila con label, slider y valor numérico."""
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=3)

            unit = self._UNITS.get(name, "")
            header = ctk.CTkFrame(row, fg_color="transparent")
            header.pack(fill="x")

            ctk.CTkLabel(
                header,
                text=name,
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                text_color="#94a3b8",
                width=50,
                anchor="w",
            ).pack(side="left")

            val_label = ctk.CTkLabel(
                header,
                text=f"{cfg['default']:.1f} {unit}",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color="#e2e8f0",
                anchor="e",
            )
            val_label.pack(side="right")
            self._value_labels[name] = val_label

            var = ctk.DoubleVar(value=cfg["default"])
            self._vars[name] = var

            ctk.CTkSlider(
                row,
                from_=cfg["from"],
                to=cfg["to"],
                variable=var,
                number_of_steps=int((cfg["to"] - cfg["from"]) / cfg["step"]),
                button_color="#00b4d8",
                button_hover_color="#0284c7",
                progress_color="#0ea5e9",
                command=lambda v, n=name: self._on_change(n, v),
            ).pack(fill="x", pady=(2, 0))

        def _on_change(self, name: str, value: float) -> None:
            """Actualiza la etiqueta del valor y dispara el callback."""
            unit = self._UNITS.get(name, "")
            self._value_labels[name].configure(text=f"{value:.1f} {unit}")
            if self._callback:
                self._callback()

        def _reset_defaults(self) -> None:
            """Restablece todos los sliders a sus valores por defecto."""
            for name, cfg in self._PARAMS.items():
                self._vars[name].set(cfg["default"])
                unit = self._UNITS.get(name, "")
                self._value_labels[name].configure(
                    text=f"{cfg['default']:.1f} {unit}"
                )
            if self._callback:
                self._callback()

        def set_callback(self, fn: Callable) -> None:
            """
            Registra la función que se llama al mover cualquier slider.

            Args:
                fn: Callable sin argumentos.
            """
            self._callback = fn

        def get_datos(self) -> dict[str, float]:
            """
            Retorna los valores actuales de los parámetros.

            Returns:
                {"Vcc": float, "Rb": float, "Rc": float, "Beta": float}
                Rb y Rc se convierten a Ohms (× 1000) antes de retornar.
            """
            return {
                "Vcc":  self._vars["Vcc"].get(),
                "Rb":   self._vars["Rb"].get() * 1_000,   # kΩ → Ω
                "Rc":   self._vars["Rc"].get() * 1_000,   # kΩ → Ω
                "Beta": self._vars["Beta"].get(),
            }


class _MockMotorCalculo:
    """
    Mock del módulo motor_calculo (Integrante 2).

    Interfaz pública esperada:
        - calcular(datos_circuito) → dict resultados
    """

    @staticmethod
    def calcular(datos: dict[str, float]) -> dict[str, dict]:
        """
        Calcula los parámetros del BJT para el modelo Ideal y la 2ª Aprox.

        Modelo Ideal (Vbe = 0 V):
            Ib  = Vcc / Rb
            Ic  = Beta * Ib
            Vce = Vcc - Ic * Rc

        Segunda Aproximación (Vbe = 0.7 V):
            Ib  = (Vcc - 0.7) / Rb
            Ic  = Beta * Ib
            Vce = Vcc - Ic * Rc

        Args:
            datos: {"Vcc": float, "Rb": float, "Rc": float, "Beta": float}

        Returns:
            {"ideal": {...}, "segunda_aprox": {...}}
        """
        vcc  = datos["Vcc"]
        rb   = datos["Rb"]
        rc   = datos["Rc"]
        beta = datos["Beta"]

        def estado_bjt(vce: float, vbe: float) -> str:
            if vbe <= 0.0 and vce > vbe:
                return "Corte"
            if vce < 0.2:
                return "Saturación"
            return "Activa"

        # ── Modelo Ideal (Vbe = 0) ──────────────────────────────────────────
        ib_ideal  = vcc / rb if rb > 0 else 0.0
        ic_ideal  = beta * ib_ideal
        vce_ideal = vcc - ic_ideal * rc

        # ── Segunda Aproximación (Vbe = 0.7 V) ─────────────────────────────
        vbe_sa    = 0.7
        ib_sa     = (vcc - vbe_sa) / rb if rb > 0 else 0.0
        ic_sa     = beta * ib_sa
        vce_sa    = vcc - ic_sa * rc

        return {
            "ideal": {
                "Vbe":    0.0,
                "Ib":     ib_ideal  * 1_000,   # A → mA
                "Ic":     ic_ideal  * 1_000,
                "Vce":    vce_ideal,
                "estado": estado_bjt(vce_ideal, 0.0),
            },
            "segunda_aprox": {
                "Vbe":    vbe_sa,
                "Ib":     ib_sa     * 1_000,
                "Ic":     ic_sa     * 1_000,
                "Vce":    vce_sa,
                "estado": estado_bjt(vce_sa, vbe_sa),
            },
        }


class _MockAnalisisOutput:
    """
    Mock del módulo analisis_output (Integrante 4).

    Interfaz pública esperada:
        - TablaResultados(master) → CTkFrame con una tabla comparativa
        - tabla.actualizar(resultados) → actualiza filas de la tabla
    """

    class TablaResultados(ctk.CTkFrame):
        """Tabla comparativa de resultados entre los dos modelos."""

        _FILAS: list[tuple[str, str, str]] = [
            ("Vbe",    "V",  "Vbe"),
            ("Ib",     "mA", "Ib"),
            ("Ic",     "mA", "Ic"),
            ("Vce",    "V",  "Vce"),
            ("Estado", "",   "estado"),
        ]

        def __init__(self, master: Any, **kwargs: Any) -> None:
            super().__init__(master, fg_color="#16213e", corner_radius=10, **kwargs)
            self._cells: dict[str, dict[str, ctk.CTkLabel]] = {
                "ideal":         {},
                "segunda_aprox": {},
            }
            self._build()

        def _build(self) -> None:
            """Construye el encabezado y filas de la tabla."""
            ctk.CTkLabel(
                self,
                text="📊  Tabla Comparativa",
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color="#e2e8f0",
            ).grid(row=0, column=0, columnspan=3, padx=14, pady=(14, 4), sticky="w")

            # Separador
            sep = ctk.CTkFrame(self, height=1, fg_color="#334155")
            sep.grid(row=1, column=0, columnspan=3, sticky="ew", padx=14, pady=(0, 8))

            # Encabezados de columna
            headers = ["Parámetro", "Ideal", "2ª Aprox."]
            colors  = ["#64748b",   "#00b4d8", "#f4a261"]
            for col, (hdr, clr) in enumerate(zip(headers, colors)):
                ctk.CTkLabel(
                    self,
                    text=hdr,
                    font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                    text_color=clr,
                ).grid(row=2, column=col, padx=8, pady=4, sticky="ew")

            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)

            # Filas de datos
            for i, (nombre, unidad, key) in enumerate(self._FILAS):
                row_idx = i + 3
                bg = "#0f172a" if i % 2 == 0 else "#1e293b"

                row_frame = ctk.CTkFrame(self, fg_color=bg, corner_radius=4)
                row_frame.grid(
                    row=row_idx, column=0, columnspan=3,
                    padx=8, pady=1, sticky="ew",
                )
                row_frame.columnconfigure(0, weight=1)
                row_frame.columnconfigure(1, weight=1)
                row_frame.columnconfigure(2, weight=1)

                display_name = f"{nombre} ({unidad})" if unidad else nombre
                ctk.CTkLabel(
                    row_frame,
                    text=display_name,
                    font=ctk.CTkFont(family="Consolas", size=10),
                    text_color="#94a3b8",
                ).grid(row=0, column=0, padx=8, pady=5, sticky="w")

                for col_idx, modelo in enumerate(["ideal", "segunda_aprox"]):
                    lbl = ctk.CTkLabel(
                        row_frame,
                        text="---",
                        font=ctk.CTkFont(family="Consolas", size=10),
                        text_color="#00b4d8" if modelo == "ideal" else "#f4a261",
                    )
                    lbl.grid(row=0, column=col_idx + 1, padx=8, pady=5)
                    self._cells[modelo][key] = lbl

        def actualizar(self, resultados: dict[str, dict]) -> None:
            """
            Actualiza el contenido de la tabla con nuevos resultados.

            Args:
                resultados: Diccionario con "ideal" y "segunda_aprox".
            """
            for modelo in ["ideal", "segunda_aprox"]:
                datos = resultados.get(modelo, {})
                for _, unidad, key in self._FILAS:
                    val = datos.get(key, "---")
                    if isinstance(val, float):
                        text = f"{val:.4f}" if unidad else f"{val:.2f}"
                    else:
                        text = str(val)
                    self._cells[modelo][key].configure(text=text)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — CARGA DINÁMICA DE MÓDULOS
# ══════════════════════════════════════════════════════════════════════════════

def _cargar_modulo(nombre: str, mock_class: type) -> Any:
    """
    Intenta importar el módulo real; si no existe, usa el Mock.

    Esto permite que main.py funcione en cualquier estado del proyecto.

    Args:
        nombre:     Nombre del módulo a importar (e.g. "motor_calculo").
        mock_class: Clase Mock de respaldo.

    Returns:
        El módulo importado o la instancia Mock.
    """
    try:
        modulo = importlib.import_module(nombre)
        print(f"  ✔ Módulo real cargado: {nombre}")
        return modulo
    except ModuleNotFoundError:
        print(f"  ⚠ Módulo '{nombre}' no encontrado → usando Mock.")
        return mock_class


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class SimuladorBJT(ctk.CTk):
    """
    Ventana raíz de la aplicación. Orquesta la comunicación entre módulos.

    Flujo de datos:
        [PanelParametros] → get_datos()
            ↓ datos_circuito: dict
        [MotorCalculo] → calcular(datos_circuito)
            ↓ resultados: dict
        [CircuitoCanvas] → actualizar_valores(resultados)
        [TablaResultados] → actualizar(resultados)
    """

    APP_TITLE   = "Simulador BJT — Ideal vs. Segunda Aproximación"
    APP_VERSION = "v1.0.0"
    WIN_W       = 1080
    WIN_H       = 660

    def __init__(self) -> None:
        super().__init__()

        # ── Configuración de la ventana ──────────────────────────────────────
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"{self.APP_TITLE}  {self.APP_VERSION}")
        self.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.resizable(False, False)
        self.configure(fg_color="#0d1117")

        # ── Carga de módulos (reales o Mock) ─────────────────────────────────
        print("\n[SimuladorBJT] Cargando módulos del equipo...")
        self._mod_ui  = _cargar_modulo("ui_arquitectura", _MockUiArquitectura)
        self._mod_cal = _cargar_modulo("motor_calculo",   _MockMotorCalculo)
        self._mod_out = _cargar_modulo("analisis_output", _MockAnalisisOutput)
        print("[SimuladorBJT] Módulos listos.\n")

        # ── Construcción de la interfaz ───────────────────────────────────────
        self._build_ui()

        # ── Cálculo inicial ───────────────────────────────────────────────────
        self._on_parametros_cambiados()

    # ──────────────────────────────────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Ensambla el layout de tres columnas de la ventana principal."""
        self._build_title_bar()

        # ── Contenedor principal de tres columnas ────────────────────────────
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Columna 1: Panel de parámetros (Integrante 1)
        self._panel_params = self._mod_ui.PanelParametros(main_frame)
        self._panel_params.pack(side="left", fill="y", padx=(0, 8))
        self._panel_params.set_callback(self._on_parametros_cambiados)

        # Columna 2: Canvas gráfico (Integrante 3 — propio)
        self._canvas_widget = visual_canvas.CircuitoCanvas(main_frame)
        self._canvas_widget.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Columna 3: Tabla de resultados (Integrante 4)
        right_col = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_col.pack(side="left", fill="y")

        self._tabla = self._mod_out.TablaResultados(right_col)
        self._tabla.pack(fill="both", expand=True)

        self._build_status_bar(right_col)

    def _build_title_bar(self) -> None:
        """Construye la barra de título personalizada."""
        bar = ctk.CTkFrame(self, fg_color="#0f172a", height=46, corner_radius=0)
        bar.pack(fill="x", padx=0, pady=0)
        bar.pack_propagate(False)

        ctk.CTkLabel(
            bar,
            text="⚡ SIMULADOR BJT",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color="#00b4d8",
        ).pack(side="left", padx=16, pady=10)

        ctk.CTkLabel(
            bar,
            text="Ideal  vs.  Segunda Aproximación",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#64748b",
        ).pack(side="left", padx=0)

        ctk.CTkLabel(
            bar,
            text=f"FISI-UNMSM  |  {self.APP_VERSION}",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#334155",
        ).pack(side="right", padx=16)

    def _build_status_bar(self, parent: ctk.CTkFrame) -> None:
        """Construye la barra de estado en la parte inferior derecha."""
        self._status_label = ctk.CTkLabel(
            parent,
            text="● Listo",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#4ade80",
            anchor="w",
        )
        self._status_label.pack(fill="x", padx=4, pady=(6, 0))

    # ──────────────────────────────────────────────────────────────────────────
    # Flujo de datos (Event handler)
    # ──────────────────────────────────────────────────────────────────────────

    def _on_parametros_cambiados(self) -> None:
        """
        Callback central disparado por cualquier cambio en los sliders.

        Orquesta el flujo completo:
            1. Leer datos del panel (Integrante 1)
            2. Calcular resultados (Integrante 2)
            3. Actualizar canvas gráfico (Integrante 3)
            4. Actualizar tabla comparativa (Integrante 4)
        """
        # 1. Lectura de parámetros
        datos_circuito: dict[str, float] = self._panel_params.get_datos()

        # 2. Cálculo
        resultados: dict[str, dict] = self._mod_cal.calcular(datos_circuito)

        # 3. Actualización del canvas
        self._canvas_widget.actualizar_valores(resultados)

        # 4. Actualización de la tabla
        self._tabla.actualizar(resultados)

        # 5. Actualizar barra de estado
        estado_ideal = resultados.get("ideal", {}).get("estado", "?")
        self._status_label.configure(
            text=f"● Calculado  |  Región activa (Ideal): {estado_ideal}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Inicializa y arranca la aplicación."""
    app = SimuladorBJT()
    app.mainloop()


if __name__ == "__main__":
    main()
