import tkinter as tk
import csv

def show_stats(self, parent):
    """
    Crea una ventana secundaria con el análisis detallado de los datos del CSV.
    """
    stats_win = tk.Toplevel(parent)
    stats_win.title("Panel de Estadísticas - KODIAK")
    stats_win.geometry("500x245")
    stats_win.resizable(False, False)
    stats_win.grab_set()

    # Configurar pesos
    stats_win.columnconfigure(0, weight=1)
    stats_win.columnconfigure(1, weight=1)

    # --- PROCESAMIENTO DE DATOS ---

    # Intentar leer el CSV y contar el número total de registros
    try:
        with open(
            self.csv_log,
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f)
            data = list(reader)

        total_records = len(data)
    except Exception:
        total_records = 0

    # --- DISEÑO DE LA INTERFAZ ---
    
    # Título
    tk.Label(
        stats_win,
        text="RESUMEN DE GESTIÓN",
        font=(
            "Helvetica",
            14,
            "bold",
        ),
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20,
    )

    # Card 1: TOTAL GENERAL
    frame_total = tk.LabelFrame(
        stats_win,
        text=" TOTAL GENERAL ",
        padx=10,
        pady=10,
    )
    frame_total.grid(
        row=1,
        column=0,
        columnspan=2,
        padx=20,
        sticky="nsew",
    )
    tk.Label(
        frame_total,
        text=f"{total_records}",
        font=(
            "Helvetica",
            24,
            "bold",
        ),
        fg="#2F5597",
    ).pack()
    tk.Label(
        frame_total,
        text="CIUDADANO(S) REGISTRADO(S) EN EL SISTEMA",
    ).pack()

    # Botón de cierre
    tk.Button(
        stats_win,
        text="Cerrar",
        width=15,
        command=stats_win.destroy,
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=20,
    )