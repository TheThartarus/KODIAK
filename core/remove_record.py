from tkinter import messagebox
import os
import shutil
import csv

def remove_record(self):
    """
    Busca un registro por CDI o nombre, pide confirmación y elimina
    tanto la carpeta como la entrada en el archivo CSV.
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
            "Por favor, ingrese el nombre o CDI para eliminar.",
        )
        return False

    records = []
    found = False
    target_folder_name = ""

    # Intentar abrir el CSV y buscar el registro
    try:
        if not os.path.exists(self.csv_log):
            messagebox.showerror(
                "Error",
                "No existe el archivo de registros.",
            )
            return False

        # Leer el CSV y construir una lista de registros excepto el que se va a eliminar
        with open(
            self.csv_log,
            mode='r',
            encoding='utf-8',
            ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Si coincide, se marca para no incluirlo en la lista nueva
                if search_term == (row["FULL NAME"] or
                                   search_term == row["ID NUMBER"]):
                    found = True
                    target_folder_name = (f"{row['ID NUMBER']} - "
                                          f"{row['FULL NAME']}")
                    # Pedir confirmación antes de seguir
                    confirm = messagebox.askyesno(
                        "Confirmar", 
                        (f"¿Está segura de eliminar a:\n{row['FULL NAME']}?"
                         f"\n\nEsta acción borrará su carpeta y archivos.")
                    )
                    if not confirm:
                        return False
                else:
                    records.append(row)

        if not found:
            messagebox.showerror(
                "No Encontrado",
                f"No se encontró ningún registro para: {search_term}",
            )
            return False

        # Construir la ruta completa a la carpeta del registro a eliminar
        folder_path = self.data_folder / target_folder_name

        # Verificar si la carpeta existe antes de intentar eliminarla
        if folder_path.exists():
            shutil.rmtree(folder_path)

        # Sobrescribir el CSV con la lista actualizada
        with open(
            self.csv_log,
            mode='w',
            newline='',
            encoding='utf-8',
            ) as f:
            # Si quedan registros, escribirlos junto con las cabeceras
            if records:
                writer = csv.DictWriter(
                    f,
                    fieldnames=records[0].keys(),
                )
                writer.writeheader()
                writer.writerows(records)
            # Si no quedan registros, escribir solo las cabeceras
            else:
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

        messagebox.showinfo(
            "Éxito",
            "Registro y carpeta eliminados correctamente."
        )

        # Limpiar los campos de entrada
        self.clear_entries()

        return True

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo completar la eliminación: {e}",
        )
        return False