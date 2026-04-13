from tkinter import messagebox
import os
import csv
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def save_record(self):
    """
    Guarda un nuevo registro en el CSV y crea la carpeta correspondiente.
    """
    # Recopilar datos de los campos de entrada
    data = {
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

    # Diccionario de traducción
    translation = {
        "name": "NOMBRE",
        "cdi": "CDI",
        "date": "FECHA DE APERTURA",
        "office": "NÚMERO DE OFICIO",
    }

    # Verificar cuáles de los campos críticos están vacíos
    critical_fields = [
        "name",
        "cdi",
        "date",
        "office"
    ]

    # Crear una lista de los nombres de los campos que están vacíos
    missing = [translation[f] for f in critical_fields if not data[f]]
    
    if missing:
        # Construir el mensaje de error con los campos faltantes
        error_message = "Los siguientes campos son " \
                        "obligatorios:\n\n• " + "\n• ".join(missing)

        messagebox.showwarning(
            "Advertencia",
            error_message,
        )
        return False

    # Manejo de campos opcionales
    if not data["phone"]:
        data["phone"] = "SIN TELÉFONO"
    if not data["job"]:
        data["job"] = "DESEMPLEADO / N/A"
    if not data["residence"]:
        data["residence"] = "NO SUMINISTRADA"

    # Definir la ruta de la carpeta
    folder_name = f"{data['cdi']} - {data['name']}"
    target_path = self.data_folder / folder_name

    try:
        # Comprobar si el registro ya existe
        if target_path.exists():
            messagebox.showerror(
                "Error",
                f"Ya existe un registro para: {data['name']}.",
            )
            return False

        # Crear carpeta y extraer Excel
        target_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Verificar que el archivo ZIP existe antes de intentar extraerlo
        if os.path.exists(self.zip_source):
            with zipfile.ZipFile(
                self.zip_source,
                'r',
            ) as z:
                # Extraer la planillaa de asistencia
                with z.open("ASISTENCIA.xlsx") as source, \
                     open(
                         target_path / "ASISTENCIA.xlsx",
                         "wb",
                    ) as target:
                        shutil.copyfileobj(
                            source,
                            target,
                        )
        else:
            messagebox.showerror(
                "Error",
                "'MODELS.zip' no encontrado.",
            )
            return False

        # Escribir en el registro CSV principal
        with open(
            self.csv_log,
            mode='a',
            newline='',
            encoding='utf-8',
        ) as f:
            writer = csv.writer(f)
            writer.writerow([
                data["name"],
                data["cdi"],
                data["date"],
                data["phone"],
                data["job"],
                data["office"],
                data["time"],
                data["residence"],
                data["attendance"],
            ])

        # --- BACKUP ---

        # Obtener la ruta de "Mis Documentos"
        documents_path = Path.home() / "Documents" / "KODIAK" / "Backup"

        # Crear la carpeta si no existe
        documents_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Nombrar del archivo con la fecha actual
        today_date = datetime.now().strftime("%Y-%m-%d")
        backup_file = documents_path / f"backup_{today_date}.csv"

        # Copiar el CSV principal al backup
        shutil.copy2(
            self.csv_log,
            backup_file,
        )

        messagebox.showinfo(
            "Éxito",
            "Registro creado exitosamente.",
        )

        self.clear_entries()
        return True

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo guardar el registro: {e}",
        )
        return False