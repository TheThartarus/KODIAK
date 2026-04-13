import tkinter as tk
from tkinter import ttk
import os
import csv
from pathlib import Path

from core.save_record import *
from core.find_record import *
from core.remove_record import *
from core.generate_certs import *
from core.export_data import *
from core.update_record import *
from core.show_stats import *
from core.show_about import *

class KodiakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KODIAK")
        self.root.geometry("715x450")
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)

        # Rutas y constantes del sistema
        self.data_folder = Path("data")
        self.csv_log = "records.csv"
        self.zip_source = "MODELS.zip"
        
        # Inicializar archivos y UI
        self.setup_system()
        self.create_widgets()

        # Declarar variable para almacenar el ID del registro buscado
        self.id_found = None

        # Manejar el cierre de la aplicación
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing,
        )

    def clear_entries(self):
        """Borra todos los campos de entrada después de guardar."""
        self.entry_full_name.delete(
            0,
            tk.END,
        )
        self.entry_id_number.delete(
            0,
            tk.END,
        )
        self.entry_phone.delete(
            0,
            tk.END,
        )
        self.entry_profession.delete(
            0,
            tk.END,
        )
        self.entry_open_date.delete(
            0,
            tk.END,
        )
        self.entry_office_no.delete(
            0,
            tk.END,
        )
        self.entry_residence.delete(
            0,
            tk.END,
        )
        self.combobox_agreed_time.current(0)
        self.combobox_attendance.current(0)

    def on_closing(self):
        if messagebox.askyesno(
            "Salir",
            "¿Desea cerrar KODIAK?",
        ):
            self.root.destroy()

    def setup_system(self):
        """Crea el directorio de datos y el registro CSV si no existen."""
        if not self.data_folder.exists():
            self.data_folder.mkdir()
            
        if not os.path.exists(self.csv_log):
            with open(
                self.csv_log,
                mode='w',
                newline='',
                encoding='utf-8',
            ) as f:
                writer = csv.writer(f)
                writer.writerow([
                    "FULL NAME",
                    "ID NUMBER",
                    "OPENING DATE",
                    "PHONE",
                    "PROFESSION",
                    "OFFICE NUMBER",
                    "AGREED TIME",
                    "RESIDENCE",
                    "ATTENDANCE",
                ])

    # Definir métodos de validación
    def validate_letters(self, text):
        """Sólo permite letras y espacios."""
        return all((c.isalpha() or
                    c.isspace() for c in text) or
                    text == ""
                )

    def validate_numbers(self, text):
        """Sólo permite dígitos numéricos."""
        return text.isdigit() or text == ""

    def validate_date(self, text):
        """Sólo permite números y barras diagonales (/)."""
        return all((c.isdigit() or
                    c == "/" for c in text) or
                    text == ""
                )

    def force_upper(self, var):
        """Fuerza los StringVar en mayúsculas."""
        current_value = var.get()
        var.set(current_value.upper())

    def create_widgets(self):
        # Registrar comandos de validación
        v_letters = self.root.register(
            self.validate_letters
        )
        v_numbers = self.root.register(
            self.validate_numbers
        )
        v_date = self.root.register(
            self.validate_date
        )
    
        # Desplegar el título
        tk.Label(
            self.root, 
            text="KODIAK", 
            font=(
                "Helvetica",
                20,
                "bold",
            ),
        ).grid(
            row=0,
            column=0,
            pady=10,
        )

        # Desplegar el contenedor
        self.container = tk.LabelFrame(
            self.root, 
            text=" DATOS ", 
            padx=15,
            pady=15,
        )
        self.container.grid(
            row=1,
            column=0,
            padx=20,
            pady=0,
            sticky="ew",
        )

        # Configurar pesos del contenedor
        self.container.columnconfigure(
            1,
            weight=1,
        )
        self.container.columnconfigure(
            3,
            weight=1,
        )

        # --- FILA 0 ---

        # Desplegar el Label de NOMBRE
        tk.Label(
            self.container,
            text="NOMBRE:",
            font=("Helvetica", 14),
        ).grid(
            row=0,
            column=0,
            pady=5,
            sticky="ew",
        )

        # Declarar variable de control con trazado para forzar mayúsculas
        self.name_var = tk.StringVar()
        self.name_var.trace_add(
            "write",
            lambda *args: self.force_upper(
                self.name_var
            )
        )

        # Desplegar el Entry de NOMBRE con validación de letras
        self.entry_full_name = tk.Entry(
            self.container, 
            width=25, 
            textvariable=self.name_var,
            validate="key", 
            validatecommand=(
                v_letters,
                "%P",
            ),
        )
        self.entry_full_name.grid(
            row=0,
            column=1,
            padx=5,
            sticky="ew",
        )

        # Desplegar el Label de CDI
        tk.Label(
            self.container,
            text="CDI:",
            font=("Helvetica", 14),
        ).grid(
            row=0,
            column=2,
            pady=5,
        )

        # Desplegar el Entry de CDI con validación de números
        self.entry_id_number = tk.Entry(
            self.container,
            width=20,
            validate="key",
            validatecommand=(
                v_numbers,
                "%P",
            ),
        )
        self.entry_id_number.grid(
            row=0,
            column=3,
            padx=5,
            sticky="ew",
        )

        # --- FILA 1 ---

        # Desplegar el Label de TELÉFONO
        tk.Label(
            self.container,
            text="TELÉFONO:",
            font=("Helvetica", 14),
            ).grid(
                row=1,
                column=0,
                pady=5,
            )

        # Desplegar el Entry de TELÉFONO con validación de números
        self.entry_phone = tk.Entry(
            self.container,
            width=25,
            validate="key",
            validatecommand=(
                v_numbers,
                "%P",
            ),
        )
        self.entry_phone.grid(
            row=1,
            column=1,
            padx=5,
            sticky="ew",
        )

        # Desplegar el Label de PROFESIÓN
        tk.Label(
            self.container,
            text="PROFESIÓN:",
            font=("Helvetica", 14),
            ).grid(
                row=1,
                column=2,
                pady=5,
            )

        # Declarar variable de control con trazado para forzar mayúsculas
        self.profession_var = tk.StringVar()
        self.profession_var.trace_add(
            "write",
            lambda *args: self.force_upper(
                self.profession_var
            )
        )

        # Desplegar el Entry de PROFESIÓN con validación de letras
        self.entry_profession = tk.Entry(
            self.container,
            width=20,
            textvariable=self.profession_var,
            validate="key",
            validatecommand=(
                v_letters,
                "%P",
            ),
        )
        self.entry_profession.grid(
            row=1,
            column=3,
            padx=5,
            sticky="ew",
        )

        # --- FILA 2 ---

        # Desplegar el Label de APERTURA
        tk.Label(
            self.container,
            text="APERTURA:",
            font=("Helvetica", 14),
            ).grid(
                row=2,
                column=0,
                pady=5,
            )

        # Desplegar el Entry de APERTURA con validación de fecha
        self.entry_open_date = tk.Entry(
            self.container,
            width=25,
            validate="key",
            validatecommand=(
                v_date,
                "%P",
            ),
        )
        self.entry_open_date.grid(
            row=2,
            column=1,
            padx=5,
            sticky="ew",
        )

        # Desplegar el Label de N° OFICIO
        tk.Label(
            self.container,
            text="N° OFICIO:",
            font=("Helvetica", 14),
            ).grid(
                row=2,
                column=2,
                pady=5,
            )

        # Desplegar el Entry de N° OFICIO con validación de números
        self.entry_office_no = tk.Entry(
            self.container,
            width=20,
            validate="key",
            validatecommand=(
                v_numbers,
                "%P",
            ),
        )
        self.entry_office_no.grid(
            row=2,
            column=3,
            padx=5,
            sticky="ew",
        )

        # --- FILA 3 ---

        # Desplegar el Label de TIEMPO
        tk.Label(
            self.container,
            text="TIEMPO:",
            font=("Helvetica", 14),
            ).grid(
                row=3,
                column=0,
                pady=5,
            )

        # Desplegar el Combobox de TIEMPO
        self.combobox_agreed_time = ttk.Combobox(
            self.container, 
            values=[
                "3 meses",
                "4 meses",
                "6 meses",
                ], 
            state="readonly", 
            width=22,
        )
        self.combobox_agreed_time.grid(
            row=3,
            column=1,
            padx=5,
            sticky="ew",
        )

        # Establecer valor por defecto en el Combobox
        self.combobox_agreed_time.current(0)

        # Desplegar el Label de RESIDENCIA
        tk.Label(
            self.container,
            text="RESIDENCIA:",
            font=("Helvetica", 14),
            ).grid(
                row=3,
                column=2,
                pady=5,
            )

        # Declarar variable de control con trazado para forzar mayúsculas
        self.residence_var = tk.StringVar()
        self.residence_var.trace_add(
            "write",
            lambda *args: self.force_upper(
                self.residence_var
            )
        )

        # Desplegar el Entry de RESIDENCIA
        self.entry_residence = tk.Entry(
            self.container,
            textvariable=self.residence_var,
            width=20,
        )
        self.entry_residence.grid(
            row=3,
            column=3,
            padx=5,
            sticky="ew",
        )

        # --- FILA 4 ---

        # Desplegar el Label de ASISTENCIAS
        tk.Label(
            self.container,
            text="ASISTENCIAS:",
            font=("Helvetica", 14),
            ).grid(
                row=4,
                column=0,
                pady=5,
            )

        # Desplegar el Combobox de ASISTENCIAS
        self.combobox_attendance = ttk.Combobox(
            self.container,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
            ],
            state="readonly",
            width=22,
        )
        self.combobox_attendance.grid(
            row=4,
            column=1,
            padx=5,
            sticky="ew",
        )

        # Establecer valor por defecto en el Combobox
        self.combobox_attendance.current(0)

        # Desplegar el Button de LIMPIAR
        self.button_clear = tk.Button(
            self.container,
            text="LIMPIAR",
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=1,
            command=lambda: self.clear_entries(),
        )
        self.button_clear.grid(
            row=4,
            column=3,
            columnspan=2,
            padx=20,
            pady=10,
            sticky="ew",
        )

        # Configurar peso
        self.container.columnconfigure(2, weight=1)

        # --- PANEL DE BOTONES ---

        # Desplegar el contenedor
        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.grid(
            row=2,
            column=0,
            columnspan=4,
            pady=10,
        )

        # Desplegar el Button de AÑADIR
        self.button_add = tk.Button(
            self.actions_frame,
            text="AÑADIR", 
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: save_record(self),
        )
        self.button_add.grid(
            row=0,
            column=0,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de ACTUALIZAR
        self.button_update = tk.Button(
            self.actions_frame,
            text="ACTUALIZAR", 
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: update_record(self),
        )
        self.button_update.grid(
            row=0,
            column=1,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de BUSCAR
        self.button_search = tk.Button(
            self.actions_frame,
            text="BUSCAR", 
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: find_record(self),
        )
        self.button_search.grid(
            row=0,
            column=2,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de ELIMINAR
        self.button_delete = tk.Button(
            self.actions_frame,
            text="ELIMINAR", 
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: remove_record(self),
        )
        self.button_delete.grid(
            row=0,
            column=3,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de CERTIFICAR
        self.button_certify = tk.Button(
            self.actions_frame, 
            text="CERTIFICAR", 
            bg= "#2e3f4f",
            fg= "#ffffff",
            width=15,
            height=2,
            command=lambda: generate_certs(self),
        )
        self.button_certify.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de EXPORTAR
        self.button_export = tk.Button(
            self.actions_frame,
            text="EXPORTAR",
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: export_data(self),
        )
        self.button_export.grid(
            row=1,
            column=1,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de ESTADÍSTICAS
        self.button_stats = tk.Button(
            self.actions_frame,
            text="ESTADÍSTICAS",
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: show_stats(self, self.root),
        )
        self.button_stats.grid(
            row=1,
            column=2,
            padx=20,
            pady=10,
        )

        # Desplegar el Button de ACERCA DE
        self.button_about = tk.Button(
            self.actions_frame,
            text="ACERCA DE",
            bg="#2e3f4f",
            fg="#ffffff",
            width=15,
            height=2,
            command=lambda: show_about(self, self.root),
        )
        self.button_about.grid(
            row=1,
            column=3,
            padx=20,
            pady=10,
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = KodiakApp(root)
    root.mainloop()