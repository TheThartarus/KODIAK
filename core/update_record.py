import csv
import os
from tkinter import messagebox

def update_record(self):
    """
    Actualiza los datos en el CSV y renombra la carpeta si es necesario.
    """
    records = []
    found = False
    old_folder_name = ""
    
    # Recopilar datos de los campos de entrada
    updated_data = {
        "name": self.entry_full_name.get().strip().upper(),
        "cdi": self.entry_id_number.get(),
        "date": self.entry_open_date.get(),
        "phone": self.entry_phone.get(),
        "job": self.entry_profession.get().strip().upper(),
        "office": self.entry_office_no.get(),
        "time": self.combobox_agreed_time.get(),
        "residence": self.entry_residence.get().strip().upper(),
        "attendance": self.combobox_attendance.get(),
    }

    # Crear el nuevo nombre de carpeta basado en los datos actualizados
    new_folder_name = f"{updated_data['cdi']} - {updated_data['name']}"

    # Verificar que los campos críticos no estén vacíos
    if not updated_data["name"] or not updated_data["cdi"]:
        messagebox.showwarning(
            "Advertencia",
            "El nombre y el CDI son obligatorios.",
        )
        return False

    # Manejo de campos opcionales
    if not self.id_found:
        messagebox.showwarning(
            "Advertencia",
            "Primero debe buscar un registro para poder actualizarlo.",
        )
        return False

    # Verificar si el nuevo CDI ya existe en otro registro
    try:
        # Leer el CSV y buscar el registro original para actualizarlo
        with open(
            self.csv_log,
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Si encontramos el registro original, lo actualizamos
                if row["ID NUMBER"] == self.id_found:
                    found = True
                    old_folder_name = (f"{row['ID NUMBER']} - "
                                       f"{row['FULL NAME']}")
                    # Reemplazar los datos viejos con los nuevos
                    records.append({
                        "FULL NAME": updated_data["name"],
                        "ID NUMBER": updated_data["cdi"],
                        "OPENING DATE": updated_data["date"],
                        "PHONE": updated_data["phone"],
                        "PROFESSION": updated_data["job"],
                        "OFFICE NUMBER": updated_data["office"],
                        "AGREED TIME": updated_data["time"],
                        "RESIDENCE": updated_data["residence"],
                        "ATTENDANCE": updated_data["attendance"],
                    })

                    messagebox.showinfo(
                        "Éxito",
                        "Registro actualizado correctamente.",
                    )

                    # Actualizar el CDI de referencia
                    self.current_editing_id = updated_data["cdi"]
                else:
                    records.append(row)

        if not found:
            messagebox.showerror(
                "Error",
                "No se encontró el registro original para actualizar.",
            )
            return False

        # Manejar la carpeta física (renombrar si es necesario)
        if old_folder_name != new_folder_name:
            old_path = self.data_folder / old_folder_name
            new_path = self.data_folder / new_folder_name

            if old_path.exists():
                if new_path.exists():
                    messagebox.showerror(
                        "Error",
                        (f"No se puede renombrar: la carpeta "
                         f"{new_folder_name} ya existe."),
                    )
                    return False
                os.rename(
                    old_path,
                    new_path,
                )

        # Sobrescribir el CSV con los datos actualizados
        with open(
            self.csv_log,
            mode='w',
            newline='',
            encoding='utf-8',
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=records[0].keys(),
            )
            writer.writeheader()
            writer.writerows(records)

        return True

    except Exception as e:
        messagebox.showerror(
            "Error de Sistema",
            f"No se pudo actualizar: {e}",
        )
        return False