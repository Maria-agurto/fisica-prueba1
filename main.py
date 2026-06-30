"""
main.py
=======
Módulo: Integrante 3 — Orquestador Principal
Proyecto: Simulador de Aproximaciones del Transistor BJT
Curso: [Nombre del curso] — FISI-UNMSM

Descripción:
    Punto de entrada del simulador BJT. Inicializa la ventana raíz de
    CustomTkinter e integra los cuatro módulos del equipo:
        - ui_arquitectura  (Integrante 1): PantallaCalculadora (sliders/inputs)
        - motor_calculo    (Integrante 2): calcular_modelos() — Ideal / 2ª Aprox.
        - visual_canvas    (Integrante 3): CircuitoCanvas — lienzo del circuito
        - analisis_output  (Integrante 4): PanelResultados — tabla comparativa

    Flujo de datos:
        Usuario pulsa "CALCULAR" en PantallaCalculadora
            → PantallaCalculadora lee los campos y construye datos_circuito
            → invoca el callback on_calcular(datos_circuito) registrado aquí
            → main.py llama a motor_calculo.calcular_modelos(datos_circuito)
            → main.py reparte `resultados` a:
                - visual_canvas.CircuitoCanvas.actualizar_valores(resultados)
                - analisis_output.PanelResultados.actualizar_tabla_resultados(resultados)
                - ui_arquitectura.PantallaCalculadora.actualizar_estado_ui(resultados)

Uso:
    python main.py

Dependencias:
    - customtkinter >= 5.2
    - ui_arquitectura, motor_calculo, analisis_output, visual_canvas (este repo)
"""

from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

import ui_arquitectura
import motor_calculo
import analisis_output
import visual_canvas


class SimuladorBJT(ctk.CTk):
    """
    Ventana raíz de la aplicación. Orquesta la comunicación entre módulos.
    """

    APP_TITLE   = "Simulador BJT — Ideal vs. Segunda Aproximación"
    APP_VERSION = "v1.0.0"
    WIN_W       = 1280
    WIN_H       = 760

    # Valores por defecto para el cálculo inicial al abrir la app
    # (coinciden con los placeholders definidos en ui_arquitectura.py).
    DATOS_INICIALES = {
        "Vcc":  9.0,
        "Rb":   75_000.0,   # 75 kΩ → Ω
        "Rc":   700.0,      # 0.7 kΩ → Ω
        "Beta": 100.0,
        "Vbe":  0.70,
    }

    def __init__(self) -> None:
        super().__init__()

        # ── Configuración de la ventana ──────────────────────────────────────
        self.title(f"{self.APP_TITLE}  {self.APP_VERSION}")
        self.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.minsize(1100, 650)

        # ── Construcción de la interfaz ───────────────────────────────────────
        self._build_ui()

        # ── Cálculo inicial con los valores por defecto de la UI ─────────────
        self._on_calcular(dict(self.DATOS_INICIALES))

    # ──────────────────────────────────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """
        Ensambla la interfaz. PantallaCalculadora (Integrante 1) ya incluye
        su propio sidebar de parámetros y un contenedor vacío reservado
        para el canvas; aquí se monta el canvas real (Integrante 3) y la
        tabla de resultados (Integrante 4) como un panel lateral adicional.
        """
        # Pantalla principal del Integrante 1 (sidebar de parámetros +
        # contenedor de canvas + header/estado).
        self._pantalla = ui_arquitectura.PantallaCalculadora(
            self,
            on_calcular=self._on_calcular,
        )
        self._pantalla.pack(side="left", fill="both", expand=True)

        # Canvas real del circuito (Integrante 3) montado dentro del
        # contenedor que expone ui_arquitectura.py.
        contenedor_canvas = self._pantalla.obtener_contenedor_canvas()
        self._canvas_widget = visual_canvas.CircuitoCanvas(contenedor_canvas)
        self._canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Panel lateral derecho con la tabla comparativa (Integrante 4).
        panel_derecho = ctk.CTkFrame(self, width=360, corner_radius=0)
        panel_derecho.pack(side="right", fill="y")
        panel_derecho.pack_propagate(False)

        self._tabla = analisis_output.PanelResultados(panel_derecho)
        self._tabla.pack(fill="both", expand=True, padx=8, pady=8)

    # ──────────────────────────────────────────────────────────────────────────
    # Flujo de datos (Event handler)
    # ──────────────────────────────────────────────────────────────────────────

    def _on_calcular(self, datos_circuito: dict) -> None:
        """
        Callback central registrado en PantallaCalculadora. Se dispara
        cuando el usuario pulsa "CALCULAR".

        Orquesta el flujo completo:
            1. Recibir datos_circuito desde la UI (Integrante 1)
            2. Calcular resultados (Integrante 2)
            3. Actualizar canvas gráfico (Integrante 3)
            4. Actualizar tabla comparativa (Integrante 4)
            5. Actualizar barra de estado (Integrante 1)

        Args:
            datos_circuito: dict con claves Vcc, Rb, Rc, Beta, Vbe
                             (Vbe no se usa en el cálculo — el motor evalúa
                             ambos modelos con Vbe=0 y Vbe=0.7 internamente).
        """
        try:
            resultados: dict = motor_calculo.calcular_modelos(datos_circuito)
        except (ZeroDivisionError, ValueError) as exc:
            messagebox.showerror(
                "Error de cálculo",
                f"No se pudo calcular el circuito: {exc}\n"
                "Verifica que Rb y Rc sean mayores a cero.",
            )
            return

        # 3. Actualización del canvas
        self._canvas_widget.actualizar_valores(resultados)

        # 4. Actualización de la tabla
        self._tabla.actualizar_tabla_resultados(resultados)

        # 5. Actualización de la barra de estado de PantallaCalculadora
        self._pantalla.actualizar_estado_ui(resultados)


def main() -> None:
    """Inicializa y arranca la aplicación."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = SimuladorBJT()
    app.mainloop()


if __name__ == "__main__":
    main()
