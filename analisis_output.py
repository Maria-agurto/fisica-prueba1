import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
import csv


class PanelResultados(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Resultados del Análisis",
            font=("Arial",18,"bold")
        )

        titulo.pack(pady=10)

        columnas = (
            "Modelo",
            "VBE (V)",
            "IB (A)",
            "IC (A)",
            "VCE (V)",
            "Estado"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=2
        )

        for columna in columnas:
            self.tabla.heading(columna,text=columna)
            self.tabla.column(columna,width=100,anchor="center")

        self.tabla.pack(fill="both",expand=True,padx=15,pady=15)

        boton = ctk.CTkButton(
            self,
            text="Exportar CSV",
            command=self.exportar_csv
        )

        boton.pack(pady=10)


    def actualizar_tabla_resultados(self,resultados):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        ideal = resultados["ideal"]

        self.tabla.insert(
            "",
            "end",
            values=(
                "Ideal",
                ideal["Vbe"],
                ideal["Ib"],
                ideal["Ic"],
                ideal["Vce"],
                ideal["estado"]
            )
        )

        segunda = resultados["segunda_aprox"]

        self.tabla.insert(
            "",
            "end",
            values=(
                "2da Aprox",
                segunda["Vbe"],
                segunda["Ib"],
                segunda["Ic"],
                segunda["Vce"],
                segunda["estado"]
            )
        )

    # Alias público — main.py invoca `actualizar()` como nombre de contrato genérico.
    actualizar = actualizar_tabla_resultados


    def exportar_csv(self):

        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV","*.csv")]
        )

        if archivo == "":
            return

        with open(archivo,"w",newline="") as f:

            escritor = csv.writer(f)

            escritor.writerow([
                "Modelo",
                "VBE",
                "IB",
                "IC",
                "VCE",
                "Estado"
            ])

            for fila in self.tabla.get_children():
                escritor.writerow(self.tabla.item(fila)["values"])


# Alias público — main.py instancia `TablaResultados(master)` como nombre
# de contrato genérico acordado en el README.
TablaResultados = PanelResultados
