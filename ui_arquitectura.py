"""
ui_arquitectura.py  —  Integrante 1: Arquitecto UI
Simulador BJT NPN | Transistor Calculator V2.0

CONTRATO DE DATOS (diccionario estándar acordado con el equipo):
─────────────────────────────────────────────────────────────────
  obtener_valores_sliders() → datos_circuito (dict)

  datos_circuito = {
      "Vcc":  float,   # Voltios         (ej. 9.0)
      "Rb":   float,   # Ohmios base     (ej. 75000.0)
      "Rc":   float,   # Ohmios colector (ej. 700.0)
      "Beta": float,   # Adimensional    (ej. 100.0)
      "Vbe":  float,   # Voltios 2da aprox (ej. 0.70)
  }

El Integrante 2 (motor_calculo.py) recibe este dict y devuelve `resultados`.
El Integrante 3 (visual_canvas.py) y el Integrante 4 (analisis_output.py)
leen `resultados`, no tocan este archivo.
─────────────────────────────────────────────────────────────────
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# ── Tema global ───────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

ACCENT   = "#BFFF00"
BG_MAIN  = "#0D0D0D"
BG_PANEL = "#1A1A1A"
BG_CARD  = "#222222"
BG_INPUT = "#2A2A2A"
TEXT_PRI = "#FFFFFF"
TEXT_SEC = "#888888"
TEXT_ACC = "#BFFF00"
BORDER   = "#333333"
GREEN_OK = "#22C55E"
RED_SAT  = "#EF4444"


# ═════════════════════════════════════════════════════════════════════════════
#  FUNCIÓN PÚBLICA — Integrante 2 la llama desde motor_calculo / main.py
# ═════════════════════════════════════════════════════════════════════════════

def obtener_valores_sliders(ui_frame: "PantallaCalculadora") -> dict:
    """
    Lee los campos de entrada de la UI y devuelve el diccionario de datos
    estándar del equipo.

    Uso desde main.py:
        datos = ui_arquitectura.obtener_valores_sliders(pantalla_calc)
        resultados = motor_calculo.calcular_modelos(datos)

    Retorna:
        datos_circuito (dict) con claves: Vcc, Rb, Rc, Beta, Vbe
        Todas las unidades en valores base (V, Ω).

    Lanza ValueError si algún campo no es un número válido.
    """
    Vcc  = float(ui_frame.entradas["Vcc  (V)"].get())
    Rb   = float(ui_frame.entradas["Rb   (kΩ)"].get()) * 1e3   # kΩ → Ω
    Rc   = float(ui_frame.entradas["Rc   (kΩ)"].get()) * 1e3   # kΩ → Ω
    Beta = float(ui_frame.entradas["β (hFE)"].get())
    Vbe  = float(ui_frame.entradas["Vbe (V)"].get())

    datos_circuito = {
        "Vcc":  Vcc,
        "Rb":   Rb,
        "Rc":   Rc,
        "Beta": Beta,
        "Vbe":  Vbe,
    }
    return datos_circuito


# ═════════════════════════════════════════════════════════════════════════════
#  CLASE PÚBLICA — Pantalla Calculadora (entrada de parámetros + canvas)
# ═════════════════════════════════════════════════════════════════════════════

class PantallaCalculadora(ctk.CTkFrame):
    """
    Pantalla principal de entrada.

    Parámetros
    ----------
    master      : ventana padre (App)
    on_calcular : callback que recibe datos_circuito (dict) y
                  llama a motor_calculo + actualiza las demás pantallas.
                  Firma: on_calcular(datos_circuito: dict) -> None
    """

    def __init__(self, master, on_calcular, **kwargs):
        super().__init__(master, fg_color=BG_MAIN, **kwargs)
        self.on_calcular = on_calcular
        self._construir()

    # ── Construcción de la UI ─────────────────────────────────────────────
    def _construir(self):
        self.grid_columnconfigure(0, weight=0)   # sidebar
        self.grid_columnconfigure(1, weight=1)   # área central
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_centro()

    def _construir_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0,
                               border_width=1, border_color=BORDER)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(20, weight=1)

        # Logo
        ctk.CTkLabel(sidebar, text="⚡ TRANSISTOR\nCALCULATOR",
                     font=("Consolas", 13, "bold"), text_color=ACCENT,
                     justify="left").grid(row=0, column=0, padx=20,
                     pady=(24, 4), sticky="w")
        ctk.CTkLabel(sidebar, text="V2.0  •  BJT NPN",
                     font=("Consolas", 10), text_color=TEXT_SEC).grid(
                     row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        _sep(sidebar, row=2)

        ctk.CTkLabel(sidebar, text="PARÁMETROS DE ENTRADA",
                     font=("Helvetica", 10, "bold"),
                     text_color=TEXT_SEC).grid(row=3, column=0,
                     padx=20, pady=(16, 8), sticky="w")

        # ── Campos de entrada — claves usadas en obtener_valores_sliders() ──
        params = [
            ("Vcc  (V)",  "9",    "Tensión de alimentación"),
            ("Rb   (kΩ)", "75",   "Resistencia de base (kΩ)"),
            ("Rc   (kΩ)", "0.7",  "Resistencia de colector (kΩ)"),
            ("β (hFE)",   "100",  "Ganancia de corriente DC"),
        ]
        self.entradas = {}
        for i, (label, default, _tooltip) in enumerate(params):
            _label_small(sidebar, label, row=4 + i * 2)
            entry = _entry(sidebar, default, row=5 + i * 2)
            self.entradas[label] = entry

        _sep(sidebar, row=13)

        ctk.CTkLabel(sidebar, text="Vbe  2DA APROX (V)",
                     font=("Helvetica", 10, "bold"),
                     text_color=TEXT_SEC).grid(row=14, column=0,
                     padx=20, pady=(16, 4), sticky="w")
        self.entry_vbe = _entry(sidebar, "0.70", row=15)
        self.entradas["Vbe (V)"] = self.entry_vbe

        _sep(sidebar, row=16)

        # Botones
        ctk.CTkButton(sidebar, text="▶  CALCULAR",
                      font=("Helvetica", 13, "bold"),
                      fg_color=ACCENT, text_color="#000000",
                      hover_color="#D4FF00", corner_radius=8,
                      command=self._on_click_calcular).grid(
                      row=17, column=0, padx=20, pady=16, sticky="ew")

        ctk.CTkButton(sidebar, text="↺  Limpiar",
                      font=("Helvetica", 11), fg_color="transparent",
                      border_width=1, border_color=BORDER,
                      text_color=TEXT_SEC, hover_color=BG_CARD,
                      corner_radius=8, command=self._reset).grid(
                      row=18, column=0, padx=20, pady=(0, 16), sticky="ew")

        self.tema_btn = ctk.CTkButton(sidebar, text="☀  Modo Claro",
                                      font=("Helvetica", 10),
                                      fg_color="transparent",
                                      border_width=1, border_color=BORDER,
                                      text_color=TEXT_SEC, hover_color=BG_CARD,
                                      corner_radius=8,
                                      command=self._toggle_tema)
        self.tema_btn.grid(row=19, column=0, padx=20, pady=(0, 24), sticky="ew")

    def _construir_centro(self):
        centro = ctk.CTkFrame(self, fg_color=BG_MAIN)
        centro.grid(row=0, column=1, sticky="nsew")
        centro.grid_columnconfigure(0, weight=1)
        centro.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(centro, fg_color=BG_PANEL, corner_radius=0,
                               border_width=1, border_color=BORDER, height=64)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(header, text="Simulador Pro  —  Transistor BJT NPN",
                     font=("Helvetica", 15, "bold"),
                     text_color=TEXT_PRI).grid(row=0, column=0,
                     padx=24, pady=18, sticky="w")
        self.estado_lbl = ctk.CTkLabel(header, text="● Listo",
                                       font=("Consolas", 11),
                                       text_color=GREEN_OK)
        self.estado_lbl.grid(row=0, column=1, padx=24, sticky="e")

        # Canvas del circuito (Integrante 3 lo reemplaza con visual_canvas.py)
        canvas_frame = ctk.CTkFrame(centro, fg_color=BG_CARD,
                                    corner_radius=12,
                                    border_width=1, border_color=BORDER)
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=28, pady=24)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(canvas_frame, text="ESQUEMA DEL CIRCUITO",
                     font=("Consolas", 11, "bold"),
                     text_color=ACCENT).grid(row=0, column=0,
                     padx=20, pady=(16, 0), sticky="w")

        self.circuit_canvas = tk.Canvas(canvas_frame, bg=BG_CARD,
                                        highlightthickness=0, height=360)
        self.circuit_canvas.grid(row=1, column=0, sticky="nsew",
                                 padx=10, pady=10)
        self.circuit_canvas.bind("<Configure>", self._dibujar_circuito)
        self.labels_dinamicos = {}

        # Footer info
        info = ctk.CTkFrame(centro, fg_color=BG_PANEL, corner_radius=0,
                             border_width=1, border_color=BORDER, height=40)
        info.grid(row=2, column=0, sticky="ew")
        info.grid_propagate(False)
        ctk.CTkLabel(info,
                     text="Modelo Ideal   •   2da Aproximación   •   Saturación",
                     font=("Helvetica", 10),
                     text_color=TEXT_SEC).pack(side="left", padx=24, pady=10)

    # ── Dibujo del circuito BJT ───────────────────────────────────────────
    def _dibujar_circuito(self, event=None):
        c = self.circuit_canvas
        c.delete("all")
        W = c.winfo_width() or 600
        H = c.winfo_height() or 360
        cx, cy = W // 2, H // 2 - 20

        lw, clr, wht, gry = 2, ACCENT, TEXT_PRI, TEXT_SEC

        def line(x1, y1, x2, y2, color=wht, width=lw):
            c.create_line(x1, y1, x2, y2, fill=color, width=width)

        def text(x, y, txt, color=ACCENT, size=10, anchor="center"):
            c.create_text(x, y, text=txt, fill=color,
                          font=("Consolas", size, "bold"), anchor=anchor)

        def resistor(x, y, vertical=True, label="R", val=""):
            if vertical:
                w = 10; sh = 8 * 6 // 2
                c.create_rectangle(x - w, y - sh, x + w, y + sh,
                                   outline=wht, width=lw, fill=BG_CARD)
            else:
                h = 10; sw = 8 * 6 // 2
                c.create_rectangle(x - sw, y - h, x + sw, y + h,
                                   outline=wht, width=lw, fill=BG_CARD)
            text(x + 22, y,      f"{label}", color=wht, size=9, anchor="w")
            text(x + 22, y + 14, val,        color=gry, size=9, anchor="w")

        def transistor_bjt(x, y):
            r = 28
            c.create_oval(x - r, y - r, x + r, y + r,
                          outline=clr, width=2, fill=BG_CARD)
            line(x - r, y, x - 10, y, color=clr)
            line(x - 10, y - 20, x - 10, y + 20, color=clr, width=3)
            line(x - 10, y - 15, x + r - 8, y - r + 8, color=clr)
            line(x - 10, y + 15, x + r - 8, y + r - 8, color=clr)
            ex, ey = x + r - 8, y + r - 8
            c.create_polygon(ex, ey, ex - 10, ey - 4, ex - 4, ey - 10,
                             fill=clr, outline=clr)
            text(x + r + 6, y,      "Q1",    color=clr, size=9, anchor="w")
            text(x + r + 6, y + 14, "BC337", color=gry, size=8, anchor="w")

        top_y, bot_y   = cy - 130, cy + 140
        left_x, right_x = cx - 180, cx + 170
        bjt_x, bjt_y   = cx + 30, cy

        line(right_x, top_y, right_x, bot_y)
        line(left_x, top_y, right_x, top_y)
        line(left_x, top_y, left_x, cy - 40)
        line(left_x, cy + 40, left_x, bot_y)
        line(left_x, bot_y, right_x, bot_y)

        for _i, (dw, dy_) in enumerate([(18, 0), (12, 7), (6, 14)]):
            c.create_line(cx, bot_y + dy_, cx + dw, bot_y + dy_, fill=wht, width=lw)
            c.create_line(cx, bot_y + dy_, cx - dw, bot_y + dy_, fill=wht, width=lw)

        text(right_x - 10, top_y - 14, "Vcc", color=clr, size=10)
        self.labels_dinamicos["Vcc"] = c.create_text(
            right_x - 10, top_y - 28, text="? V",
            fill=wht, font=("Consolas", 9), anchor="center")

        resistor(left_x,  cy,       vertical=True,  label="RB", val="")
        line(left_x, cy - 40, left_x, cy - 28)
        line(left_x, cy + 28, left_x, cy + 40)

        resistor(right_x, cy - 60, vertical=True,  label="RC", val="")
        line(right_x, top_y, right_x, cy - 88)
        line(right_x, cy - 32, right_x, bjt_y - 18)

        transistor_bjt(bjt_x, bjt_y)
        line(left_x, cy, bjt_x - 28, cy, color=clr)
        text(cx - 60, cy - 14, "VB", color=gry, size=9)
        line(bjt_x + 20, bjt_y - 20, right_x, bjt_y - 60, color=clr)
        line(bjt_x + 20, bjt_y + 20, bjt_x + 20, bot_y, color=clr)
        line(bjt_x + 20, bot_y, right_x, bot_y)
        text(bjt_x - 55, bjt_y + 50, "VBE", color=gry, size=9)

        self.labels_dinamicos["VCE"] = c.create_text(
            bjt_x + 70, bjt_y + 10, text="Vce = ---",
            fill=clr, font=("Consolas", 9))
        self.labels_dinamicos["IC"] = c.create_text(
            bjt_x + 70, bjt_y + 26, text="Ic  = ---",
            fill=clr, font=("Consolas", 9))
        self.labels_dinamicos["STATUS"] = c.create_text(
            bjt_x, bjt_y - 60, text="",
            fill=GREEN_OK, font=("Consolas", 10, "bold"))

    # ── Actualiza etiquetas del canvas con el dict `resultados` ──────────
    def actualizar_etiquetas(self, resultados: dict):
        """
        Recibe el dict `resultados` del Integrante 2 y actualiza las
        etiquetas dinámicas del canvas.

        Claves usadas: resultados["segunda_aprox"]["Vce"],
                       resultados["segunda_aprox"]["Ic"],
                       resultados["segunda_aprox"]["estado"],
                       datos_circuito["Vcc"]  (guardado internamente)
        """
        c = self.circuit_canvas
        if not self.labels_dinamicos:
            return

        aprox    = resultados["segunda_aprox"]
        Vce      = aprox["Vce"]
        Ic_mA    = aprox["Ic"] * 1e3          # A → mA para mostrar
        saturado = aprox["estado"] == "Saturación"
        Vcc_val  = resultados.get("_Vcc_entrada", "?")  # guardado en _on_click

        c.itemconfig(self.labels_dinamicos["VCE"],  text=f"Vce = {Vce:.2f} V")
        c.itemconfig(self.labels_dinamicos["IC"],   text=f"Ic  = {Ic_mA:.2f} mA")
        c.itemconfig(self.labels_dinamicos["Vcc"],  text=f"{Vcc_val} V")

        if saturado:
            c.itemconfig(self.labels_dinamicos["STATUS"],
                         text="⚠ SATURADO", fill=RED_SAT)
            self.estado_lbl.configure(text="⚠ Saturado", text_color=RED_SAT)
        else:
            c.itemconfig(self.labels_dinamicos["STATUS"],
                         text="✔ ACTIVO", fill=GREEN_OK)
            self.estado_lbl.configure(text="✔ Activo — Región Activa",
                                      text_color=GREEN_OK)

    # ── Botón CALCULAR ────────────────────────────────────────────────────
    def _on_click_calcular(self):
        """
        1. Lee la UI → datos_circuito (dict estándar).
        2. Llama a on_calcular(datos_circuito) — el orquestador main.py
           se encarga de invocar motor_calculo y actualizar las pantallas.
        """
        try:
            datos_circuito = obtener_valores_sliders(self)
        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "Verifica que todos los campos sean números válidos.")
            return

        self.on_calcular(datos_circuito)

    def _reset(self):
        defaults = {"Vcc  (V)": "9", "Rb   (kΩ)": "75",
                    "Rc   (kΩ)": "0.7", "β (hFE)": "100", "Vbe (V)": "0.70"}
        for key, val in defaults.items():
            self.entradas[key].delete(0, "end")
            self.entradas[key].insert(0, val)
        c = self.circuit_canvas
        for key in ("VCE", "IC", "STATUS"):
            if key in self.labels_dinamicos:
                c.itemconfig(self.labels_dinamicos[key],
                             text="---" if key != "STATUS" else "")
        self.estado_lbl.configure(text="● Listo", text_color=GREEN_OK)

    def _toggle_tema(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema_btn.configure(text="🌙  Modo Oscuro")
        else:
            ctk.set_appearance_mode("Dark")
            self.tema_btn.configure(text="☀  Modo Claro")


# ═════════════════════════════════════════════════════════════════════════════
#  Helpers internos de UI
# ═════════════════════════════════════════════════════════════════════════════

def _sep(parent, row):
    ctk.CTkFrame(parent, fg_color=BORDER, height=1).grid(
        row=row, column=0, sticky="ew", padx=16, pady=4)

def _label_small(parent, text, row):
    ctk.CTkLabel(parent, text=text, font=("Helvetica", 10, "bold"),
                 text_color=TEXT_SEC).grid(
                 row=row, column=0, padx=20, pady=(10, 2), sticky="w")

def _entry(parent, default, row):
    entry = ctk.CTkEntry(parent, placeholder_text=default,
                         font=("Consolas", 12), fg_color=BG_INPUT,
                         border_color=BORDER, text_color=TEXT_PRI,
                         corner_radius=6)
    entry.insert(0, default)
    entry.grid(row=row, column=0, padx=20, pady=(0, 4), sticky="ew")
    return entry


##para q ejecute solo
if __name__ == "__main__":

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("Simulador BJT")
            self.geometry("1200x700")

            pantalla = PantallaCalculadora(
                self,
                on_calcular=self.calcular
            )

            pantalla.pack(fill="both", expand=True)

        def calcular(self, datos):
            print("Datos recibidos:")
            print(datos)

    app = App()
    app.mainloop()