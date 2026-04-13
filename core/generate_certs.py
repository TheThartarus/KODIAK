from tkinter import messagebox
import os
import zipfile
import shutil

def generate_certs(self):
    """
    Busca la carpeta del imputado y extrae los modelos de Word desde el ZIP.
    """
    # Recopilar datos de los campos de entrada
    id_number = self.entry_id_number.get()
    full_name = self.entry_full_name.get().strip().upper()

    # Validar que se hayan ingresado ambos campos
    if not id_number or not full_name:
        messagebox.showwarning(
            "Advertencia",
            "Por favor, ingrese el nombre y el CDI para certificar.",
        )
        return False

    # Formatear el nombre de la carpeta
    folder_name = f"{id_number} - {full_name.upper()}"
    target_path = self.data_folder / folder_name

    # Verificar si la carpeta existe
    if not target_path.exists():
        messagebox.showerror(
            "Error",
            f"No se encontró la carpeta:\n{folder_name}",
        )
        return False

    # Extraer los modelos de Word desde el ZIP a la carpeta
    try:
        if os.path.exists(self.zip_source):
            with zipfile.ZipFile(
                self.zip_source,
                'r',
            ) as z:
                # Lista de archivos a extraer
                models = [
                    "CERTIFICACIÓN.docx",
                    "REMISIÓN.docx",
                ]

                # Verificar que los archivos existan en el ZIP
                for model in models:
                    with z.open(model) as source, \
                         open(
                             target_path / model,
                             "wb",
                         ) as target:
                        # Copiar el contenido del archivo del ZIP al destino
                        shutil.copyfileobj(
                            source,
                            target,
                        )

            messagebox.showinfo(
                "Éxito",
                "Certificación generada.",
            )

            # Abrir la carpeta
            os.startfile(target_path)

            return True
        else:
            messagebox.showerror(
                "Error",
                f"No se encontró el archivo {self.zip_source}",
            )
            return False

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Error al generar certificados: {e}",
        )
        return False