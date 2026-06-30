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
import ui_arquitectura  # <--- AGREGAR (Integrante 1)
import motor_calculo  # <--- AGREGAR (Integrante 2)
import analisis_output  # <--- AGREGAR (Integrante 4)


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

        # ── Asignación de módulos reales del equipo ──────────────────────────
        print("\n[SimuladorBJT] Enlazando módulos reales del equipo...")
        self._mod_ui  = ui_arquitectura
        self._mod_cal = motor_calculo
        self._mod_out = analisis_output
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
