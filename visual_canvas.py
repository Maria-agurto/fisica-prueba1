"""
visual_canvas.py
================
Módulo: Integrante 3 — Lienzo Gráfico del Simulador BJT
Proyecto: Simulador de Aproximaciones del Transistor BJT
Curso: [Nombre del curso] — FISI-UNMSM

Descripción:
    Define la clase CircuitoCanvas, un frame de CustomTkinter que dibuja
    de forma nativa (sin imágenes externas) el esquema de polarización fija
    del transistor BJT y muestra de manera dinámica los valores calculados
    para el modelo Ideal y la Segunda Aproximación.

Dependencias:
    - customtkinter
    - tkinter (stdlib)
"""

import tkinter as tk
from typing import Any
import customtkinter as ctk


# ──────────────────────────────────────────────────────────────────────────────
# Paleta de colores centralizada
# ──────────────────────────────────────────────────────────────────────────────
PALETTE = {
    "bg":           "#1a1a2e",   # Fondo principal
    "panel":        "#16213e",   # Fondo del canvas
    "ideal":        "#00b4d8",   # Azul — modelo ideal
    "segunda":      "#f4a261",   # Naranja — segunda aproximación
    "wire":         "#e2e8f0",   # Blanco hueso — cables del circuito
    "component":    "#94a3b8",   # Gris claro — cuerpo de componentes
    "label_bg":     "#0f3460",   # Fondo de etiquetas de valor
    "text_dim":     "#64748b",   # Texto secundario / deshabilitado
    "vcc":          "#4ade80",   # Verde — nodo Vcc
    "gnd":          "#f87171",   # Rojo — nodo GND
    "active":       "#a78bfa",   # Violeta — zona activa del BJT
}

# Dimensiones internas del canvas
CANVAS_W = 640
CANVAS_H = 460


class CircuitoCanvas(ctk.CTkFrame):
    """
    Frame de CustomTkinter que contiene un Canvas de Tkinter con el esquema
    gráfico del circuito de polarización fija BJT.

    El circuito dibujado es:
        Vcc ──┬── Rc ── Colector (C)
              │                |
             Rb              [BJT NPN]
              │                |
              └── Base (B)   Emisor (E) ── GND

    Se dibujan dos columnas de etiquetas superpuestas (Ideal | 2ª Aprox.)
    que se actualizan con cada llamada a `actualizar_valores()`.
    """

    def __init__(self, master: Any, **kwargs: Any) -> None:
        """
        Inicializa el frame y construye todos los elementos gráficos estáticos.

        Args:
            master: Widget padre de CustomTkinter.
            **kwargs: Argumentos adicionales pasados a CTkFrame.
        """
        super().__init__(master, fg_color=PALETTE["bg"], **kwargs)

        # IDs de los ítems de texto dinámicos del canvas (se actualizan luego)
        self._ids_ideal:    dict[str, int] = {}
        self._ids_segunda:  dict[str, int] = {}

        self._build_header()
        self._build_canvas()
        self._draw_static_circuit()
        self._draw_value_panels()

    # ──────────────────────────────────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────────────────────────────────

    def _build_header(self) -> None:
        """Crea el encabezado con el título del módulo y la leyenda de colores."""
        header = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=8)
        header.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            header,
            text="⚡ Esquema de Polarización Fija — BJT NPN",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=PALETTE["wire"],
        ).pack(side="left", padx=14, pady=8)

        # Leyenda de colores
        legend_frame = ctk.CTkFrame(header, fg_color="transparent")
        legend_frame.pack(side="right", padx=14)

        for label, color in [("● Ideal", PALETTE["ideal"]),
                              ("● 2ª Aprox.", PALETTE["segunda"])]:
            ctk.CTkLabel(
                legend_frame,
                text=label,
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=color,
            ).pack(side="left", padx=6)

    def _build_canvas(self) -> None:
        """Crea el widget Canvas de Tkinter dentro del frame."""
        canvas_frame = ctk.CTkFrame(self, fg_color=PALETTE["panel"], corner_radius=8)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._canvas = tk.Canvas(
            canvas_frame,
            width=CANVAS_W,
            height=CANVAS_H,
            bg=PALETTE["panel"],
            highlightthickness=0,
            bd=0,
        )
        self._canvas.pack(fill="both", expand=True, padx=4, pady=4)

    # ──────────────────────────────────────────────────────────────────────────
    # Dibujo del circuito estático
    # ──────────────────────────────────────────────────────────────────────────

    def _draw_static_circuit(self) -> None:
        """
        Dibuja todos los elementos fijos del circuito: cables, componentes
        (Rb, Rc, BJT) y nodos (Vcc, GND, Base, Colector, Emisor).

        Coordenadas de referencia (cx, cy) = (200, 230) — centro del BJT.
        """
        c = self._canvas
        cx, cy = 200, 230   # Centro del símbolo BJT

        # ── Nodo Vcc (arriba) ────────────────────────────────────────────────
        vcc_x, vcc_y = cx, 40
        self._draw_vcc_node(vcc_x, vcc_y)

        # ── Cable vertical Vcc → nodo de split ──────────────────────────────
        split_y = 90
        c.create_line(vcc_x, vcc_y + 20, vcc_x, split_y,
                      fill=PALETTE["wire"], width=2)

        # ── Nodo de bifurcación (Vcc → Rc y Vcc → Rb) ───────────────────────
        rb_x = cx - 90   # Rama izquierda (Rb)
        rc_x = cx + 60   # Rama derecha (Rc)

        c.create_line(vcc_x, split_y, rb_x, split_y,
                      fill=PALETTE["wire"], width=2)   # hacia Rb
        c.create_line(vcc_x, split_y, rc_x, split_y,
                      fill=PALETTE["wire"], width=2)   # hacia Rc

        # ── Resistencia Rb (izquierda, vertical) ────────────────────────────
        rb_top = split_y
        rb_bot = cy - 10
        self._draw_resistor(c, rb_x, rb_top, rb_x, rb_bot, "Rb")

        # ── Cable Rb → Base ──────────────────────────────────────────────────
        base_y = cy
        c.create_line(rb_x, rb_bot, rb_x, base_y,
                      fill=PALETTE["wire"], width=2)
        c.create_line(rb_x, base_y, cx - 30, base_y,
                      fill=PALETTE["wire"], width=2)

        # ── Resistencia Rc (derecha, vertical) ──────────────────────────────
        rc_top = split_y
        rc_bot = cy - 40
        self._draw_resistor(c, rc_x, rc_top, rc_x, rc_bot, "Rc")

        # ── Cable Rc → Colector ──────────────────────────────────────────────
        col_y = cy - 30
        c.create_line(rc_x, rc_bot, rc_x, col_y,
                      fill=PALETTE["wire"], width=2)
        c.create_line(rc_x, col_y, cx + 18, col_y,
                      fill=PALETTE["wire"], width=2)

        # ── Símbolo BJT NPN ──────────────────────────────────────────────────
        self._draw_bjt_npn(cx, cy)

        # ── Emisor → GND ─────────────────────────────────────────────────────
        emi_y = cy + 40
        gnd_y = emi_y + 55
        c.create_line(cx, emi_y, cx, gnd_y,
                      fill=PALETTE["wire"], width=2)
        self._draw_gnd_node(cx, gnd_y)

        # ── Etiquetas de nodos ───────────────────────────────────────────────
        c.create_text(rb_x, base_y - 14,
                      text="B", fill=PALETTE["ideal"],
                      font=("Consolas", 10, "bold"))
        c.create_text(rc_x + 14, col_y,
                      text="C", fill=PALETTE["ideal"],
                      font=("Consolas", 10, "bold"))
        c.create_text(cx + 16, emi_y + 10,
                      text="E", fill=PALETTE["ideal"],
                      font=("Consolas", 10, "bold"))

    def _draw_resistor(
        self,
        canvas: tk.Canvas,
        x1: int, y1: int,
        x2: int, y2: int,
        label: str,
    ) -> None:
        """
        Dibuja una resistencia esquemática (rectángulo con zigzag simplificado).

        Args:
            canvas: El widget Canvas.
            x1, y1: Coordenada inicial (terminal superior).
            x2, y2: Coordenada final (terminal inferior).
            label:  Nombre de la resistencia.
        """
        mid_y   = (y1 + y2) // 2
        half_h  = abs(y2 - y1) // 4
        half_w  = 14

        # Líneas de conexión superior e inferior
        canvas.create_line(x1, y1, x1, mid_y - half_h,
                           fill=PALETTE["wire"], width=2)
        canvas.create_line(x1, mid_y + half_h, x1, y2,
                           fill=PALETTE["wire"], width=2)

        # Cuerpo rectangular de la resistencia
        canvas.create_rectangle(
            x1 - half_w, mid_y - half_h,
            x1 + half_w, mid_y + half_h,
            fill="#1e293b",
            outline=PALETTE["component"],
            width=2,
        )

        # Etiqueta del componente
        canvas.create_text(
            x1 + half_w + 24, mid_y,
            text=label,
            fill=PALETTE["component"],
            font=("Consolas", 10, "bold"),
            anchor="w",
        )

    def _draw_bjt_npn(self, cx: int, cy: int) -> None:
        """
        Dibuja el símbolo estándar de un BJT NPN centrado en (cx, cy).

        Args:
            cx, cy: Centro del símbolo.
        """
        c = self._canvas

        # Línea vertical de base (body)
        c.create_line(cx - 20, cy - 35, cx - 20, cy + 35,
                      fill=PALETTE["active"], width=3)

        # Terminal Base (horizontal)
        c.create_line(cx - 30, cy, cx - 20, cy,
                      fill=PALETTE["active"], width=2)

        # Terminal Colector (diagonal, con flecha)
        c.create_line(cx - 20, cy - 18, cx + 18, cy - 30,
                      fill=PALETTE["active"], width=2)

        # Terminal Emisor (diagonal, con flecha → NPN)
        c.create_line(cx - 20, cy + 18, cx + 18, cy + 40,
                      fill=PALETTE["active"], width=2)

        # Flecha de emisor (indica tipo NPN)
        arrow_tip = (cx + 18, cy + 40)
        c.create_polygon(
            arrow_tip[0], arrow_tip[1],
            arrow_tip[0] - 10, arrow_tip[1] - 6,
            arrow_tip[0] - 6, arrow_tip[1] - 12,
            fill=PALETTE["active"],
            outline=PALETTE["active"],
        )

        # Círculo del encapsulado
        r = 42
        c.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline=PALETTE["active"],
            width=2,
            fill="",
        )

        # Etiqueta BJT
        c.create_text(
            cx + r + 12, cy,
            text="BJT\nNPN",
            fill=PALETTE["active"],
            font=("Consolas", 9, "bold"),
            anchor="w",
            justify="center",
        )

    def _draw_vcc_node(self, x: int, y: int) -> None:
        """Dibuja el símbolo de fuente de alimentación Vcc."""
        c = self._canvas
        c.create_line(x - 12, y + 20, x + 12, y + 20,
                      fill=PALETTE["vcc"], width=3)
        c.create_line(x - 8, y + 26, x + 8, y + 26,
                      fill=PALETTE["vcc"], width=2)
        c.create_line(x - 4, y + 32, x + 4, y + 32,
                      fill=PALETTE["vcc"], width=1)
        c.create_text(x, y + 8,
                      text="Vcc",
                      fill=PALETTE["vcc"],
                      font=("Consolas", 11, "bold"))

    def _draw_gnd_node(self, x: int, y: int) -> None:
        """Dibuja el símbolo de tierra (GND)."""
        c = self._canvas
        c.create_line(x - 14, y, x + 14, y,
                      fill=PALETTE["gnd"], width=3)
        c.create_line(x - 9,  y + 6,  x + 9,  y + 6,
                      fill=PALETTE["gnd"], width=2)
        c.create_line(x - 4,  y + 12, x + 4,  y + 12,
                      fill=PALETTE["gnd"], width=1)
        c.create_text(x + 22, y + 6,
                      text="GND",
                      fill=PALETTE["gnd"],
                      font=("Consolas", 10, "bold"))

    # ──────────────────────────────────────────────────────────────────────────
    # Paneles de valores dinámicos
    # ──────────────────────────────────────────────────────────────────────────

    def _draw_value_panels(self) -> None:
        """
        Dibuja los paneles de valores en la mitad derecha del canvas.
        Crea los ítems de texto con valores por defecto '---' y almacena
        sus IDs para actualización posterior.
        """
        c = self._canvas

        # ── Panel Modelo Ideal ───────────────────────────────────────────────
        self._draw_panel_box(
            x=350, y=50, w=130, h=170,
            title="Modelo Ideal",
            color=PALETTE["ideal"],
        )
        self._ids_ideal = self._create_value_rows(
            x=415, y_start=100, color=PALETTE["ideal"]
        )

        # ── Panel 2ª Aproximación ────────────────────────────────────────────
        self._draw_panel_box(
            x=500, y=50, w=130, h=170,
            title="2ª Aprox.",
            color=PALETTE["segunda"],
        )
        self._ids_segunda = self._create_value_rows(
            x=565, y_start=100, color=PALETTE["segunda"]
        )

        # ── Etiquetas de fila (compartidas) ──────────────────────────────────
        labels = ["Vbe", "Ib", "Ic", "Vce", "Estado"]
        y_pos  = [100, 122, 144, 166, 188]
        for lbl, y in zip(labels, y_pos):
            c.create_text(
                330, y,
                text=f"{lbl}:",
                fill=PALETTE["text_dim"],
                font=("Consolas", 10, "bold"),
                anchor="e",
            )

        # ── Panel de estado de saturación / corte ────────────────────────────
        self._draw_panel_box(
            x=350, y=240, w=280, h=180,
            title="Información del Punto Q",
            color=PALETTE["component"],
        )
        self._ids_estado_ideal   = self._create_estado_detalle(415, color=PALETTE["ideal"])
        self._ids_estado_segunda = self._create_estado_detalle(540, color=PALETTE["segunda"])

    def _draw_panel_box(
        self,
        x: int, y: int,
        w: int, h: int,
        title: str,
        color: str,
    ) -> None:
        """Dibuja un panel con borde coloreado y título."""
        c = self._canvas
        c.create_rectangle(
            x, y, x + w, y + h,
            fill="#0f172a",
            outline=color,
            width=1,
        )
        # Barra de título
        c.create_rectangle(
            x, y, x + w, y + 22,
            fill=color + "33",   # transparencia simulada con hex
            outline=color,
            width=1,
        )
        c.create_text(
            x + w // 2, y + 11,
            text=title,
            fill=color,
            font=("Consolas", 10, "bold"),
        )

    def _create_value_rows(
        self,
        x: int,
        y_start: int,
        color: str,
    ) -> dict[str, int]:
        """
        Crea ítems de texto para cada magnitud y retorna su diccionario de IDs.

        Args:
            x:       Coordenada X central de la columna.
            y_start: Coordenada Y del primer valor.
            color:   Color del texto.

        Returns:
            Diccionario {"vbe": id, "ib": id, "ic": id, "vce": id, "estado": id}
        """
        c   = self._canvas
        ids = {}
        magnitudes = ["vbe", "ib", "ic", "vce", "estado"]
        step = 22

        for i, key in enumerate(magnitudes):
            item_id = c.create_text(
                x, y_start + i * step,
                text="---",
                fill=color,
                font=("Consolas", 10),
                anchor="center",
            )
            ids[key] = item_id

        return ids

    def _create_estado_detalle(self, x: int, color: str) -> dict[str, int]:
        """
        Crea ítems de texto para el panel de estado inferior.

        Args:
            x:     Coordenada X.
            color: Color del texto.

        Returns:
            Diccionario con IDs de texto para el panel de detalle.
        """
        c    = self._canvas
        ids  = {}
        keys = ["region", "potencia"]
        y0   = 285

        for i, key in enumerate(keys):
            item_id = c.create_text(
                x, y0 + i * 22,
                text="---",
                fill=color,
                font=("Consolas", 10),
                anchor="center",
                width=110,
            )
            ids[key] = item_id

        return ids

    # ──────────────────────────────────────────────────────────────────────────
    # API pública
    # ──────────────────────────────────────────────────────────────────────────

    def actualizar_valores(self, resultados: dict[str, dict]) -> None:
        """
        Actualiza dinámicamente todas las etiquetas del canvas con los
        resultados calculados por el motor de cálculo (Integrante 2).

        Args:
            resultados: Diccionario con la estructura:
                {
                    "ideal": {
                        "Vbe": float, "Ib": float, "Ic": float,
                        "Vce": float, "estado": str
                    },
                    "segunda_aprox": {
                        "Vbe": float, "Ib": float, "Ic": float,
                        "Vce": float, "estado": str
                    }
                }
        """
        ideal    = resultados.get("ideal",          {})
        segunda  = resultados.get("segunda_aprox",  {})

        self._actualizar_modelo(self._ids_ideal,   ideal)
        self._actualizar_modelo(self._ids_segunda, segunda)
        self._actualizar_estado_detalle(ideal,   self._ids_estado_ideal)
        self._actualizar_estado_detalle(segunda, self._ids_estado_segunda)

    def _actualizar_modelo(
        self,
        ids: dict[str, int],
        datos: dict[str, Any],
    ) -> None:
        """
        Actualiza las etiquetas de un modelo (ideal o segunda aproximación).

        Args:
            ids:   IDs de los ítems de texto del canvas.
            datos: Sub-diccionario del modelo con los valores calculados.
        """
        c = self._canvas

        def fmt_v(key: str, unit: str = "V") -> str:
            val = datos.get(key)
            return f"{val:.4f} {unit}" if val is not None else "---"

        c.itemconfigure(ids["vbe"],    text=fmt_v("Vbe"))
        c.itemconfigure(ids["ib"],     text=fmt_v("Ib",  "mA"))
        c.itemconfigure(ids["ic"],     text=fmt_v("Ic",  "mA"))
        c.itemconfigure(ids["vce"],    text=fmt_v("Vce"))
        c.itemconfigure(ids["estado"], text=datos.get("estado", "---"))

    def _actualizar_estado_detalle(
        self,
        datos: dict[str, Any],
        ids:   dict[str, int],
    ) -> None:
        """
        Actualiza el panel inferior de información del Punto Q.

        Args:
            datos: Sub-diccionario del modelo.
            ids:   IDs del panel de detalle.
        """
        c = self._canvas
        estado = datos.get("estado", "")

        region = {
            "Activa":      "Región Activa",
            "Saturación":  "Saturación",
            "Corte":       "Corte",
        }.get(estado, "Indeterminado")

        ic  = datos.get("Ic",  0.0)
        vce = datos.get("Vce", 0.0)
        p   = ic * vce if ic and vce else 0.0

        c.itemconfigure(ids["region"],   text=f"Región: {region}")
        c.itemconfigure(ids["potencia"], text=f"P = {p:.4f} W")
