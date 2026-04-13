import tkinter as tk
from tkinter import messagebox
import csv
import os

def find_record(self):
    """
    Busca un registro en el CSV por nombre o CDI.
    Si se encuentra, devuelve el nombre de la carpeta para abrirla.
    """
    # Obtener el término de búsqueda (CDI)
    search_term = self.entry_id_number.get()

    # Si el campo de CDI está vacío, usar el nombre como término de búsqueda
    if not search_term:
        search_term = self.entry_full_name.get().strip().upper()

    # Validar que se haya ingresado un término de búsqueda
    if not search_term:
        messagebox.showwarning(
            "Advertencia",
            "Por favor, ingrese el nombre o CDI para buscar.",
        )
        return None

    found_record = None

    # Intentar abrir el CSV y buscar el registro
    try:
        with open(
            self.csv_log,
            mode='r',
            encoding='utf-8',
            ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Buscar en las columnas el nombre y el CDI
                if search_term in (
                    row["FULL NAME"],
                    row["ID NUMBER"],
                    ):
                    found_record = row
                    break

        # Si se encuentra el registro, abrir la carpeta correspondiente
        if found_record:
            # Formatear el nombre de la carpeta
            # Formato: "CDI - NOMBRE"
            folder_name = (
                f"{found_record['ID NUMBER']} - "
                f"{found_record['FULL NAME']}"
            )

            # Construir la ruta completa a la carpeta
            folder_path = self.data_folder / folder_name

            # Guardar el ID encontrado para futuras operaciones
            self.id_found = found_record["ID NUMBER"]  

            # Verificar si la carpeta existe antes de intentar abrirla
            if folder_path.exists():
                # Rellenar los campos con los datos encontrados
                self.entry_full_name.delete(
                    0,
                    tk.END,
                )
                self.entry_full_name.insert(
                    0,
                    found_record["FULL NAME"],
                )

                self.entry_id_number.delete(
                    0,
                    tk.END,
                )
                self.entry_id_number.insert(
                    0,
                    found_record["ID NUMBER"],
                )

                self.entry_phone.delete(
                    0,
                    tk.END,
                )
                self.entry_phone.insert(
                    0,
                    found_record["PHONE"],
                )
                
                self.entry_profession.delete(
                    0,
                    tk.END,
                )
                self.entry_profession.insert(
                    0,
                    found_record["PROFESSION"],
                )

                self.entry_office_no.delete(
                    0,
                    tk.END,
                )
                self.entry_office_no.insert(
                    0,
                    found_record["OFFICE NUMBER"],
                )
                
                self.entry_open_date.delete(
                    0,
                    tk.END,
                )
                self.entry_open_date.insert(
                    0,
                    found_record["OPENING DATE"],
                )

                self.entry_residence.delete(
                    0,
                    tk.END,
                )
                self.entry_residence.insert(
                    0,
                    found_record["RESIDENCE"],
                )
                self.combobox_agreed_time.set(
                    found_record["AGREED TIME"],
                )
                self.combobox_attendance.set(
                    found_record["ATTENDANCE"],
                )

                messagebox.showinfo(
                    "Éxito",
                    "Coincidencia encontrada en el registro",
                )

                # Abrir la carpeta del registro encontrado
                os.startfile(folder_path)

                return True
            else:
                messagebox.showerror(
                    "Error",
                    f"Carpeta no encontrada: {folder_name}",
                )
                return False
        else:
            messagebox.showerror(
                "Error",
                "No hay coincidencias en el registro",
            )
            return False

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Error durante la búsqueda: {e}",
        )
        return False