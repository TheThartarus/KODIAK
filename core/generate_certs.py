from tkinter import messagebox
from docx import Document
from datetime import date
import os
import zipfile
import shutil

def generate_certs(self):
    """
    Busca la carpeta del imputado y extrae los modelos de Word desde el ZIP.
    """
    today_date = date.today()

    month_names = [
        "",
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]

    # Calcular la diferencia de años para cada fecha importante
    INDEPENDENCE_DAY = date(1810, 7, 5)
    ind_year_diff = today_date.year - INDEPENDENCE_DAY.year

    FEDERATION_DAY = date(1860, 2, 20)
    fed_year_diff = today_date.year - FEDERATION_DAY.year

    REVOLUTION_DAY = date(1999, 2, 2)
    rev_year_diff = today_date.year - REVOLUTION_DAY.year

    # Ajustar las diferencias de años
    # Si la fecha actual es anterior a la fecha importante en el año
    if (today_date.month,
        today_date.day) < (INDEPENDENCE_DAY.month,
                           INDEPENDENCE_DAY.day):
        ind_year_diff -= 1

    if (today_date.month,
        today_date.day) < (FEDERATION_DAY.month,
                           FEDERATION_DAY.day):
        fed_year_diff -= 1

    if (today_date.month,
        today_date.day) < (REVOLUTION_DAY.month,
                           REVOLUTION_DAY.day):
        rev_year_diff -= 1

    year_diffs = {
        "INDEPENDENCE": ind_year_diff,
        "FEDERATION": fed_year_diff,
        "REVOLUTION": rev_year_diff,
    }

    # Recopilar datos de los campos de entrada
    data = {
        "name": self.entry_full_name.get().strip().upper(),
        "id_number": self.entry_id_number.get(),
        "open_date": self.entry_open_date.get(),
        "office_no": self.entry_office_no.get(),
    }

    # Verificar que los campos críticos no estén vacíos
    if not data["name"] or not data["id_number"]:
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

    # Formatear el nombre de la carpeta
    folder_name = f"{data['id_number']} - {data['name']}"
    target_path = self.data_folder / folder_name

    # Formatear el número de identificación con puntos
    if len(data["id_number"]) == 9:
        data["id_number"] = (data["id_number"][:3] +
                             "." +
                             data["id_number"][3:6] +
                             "." +
                             data["id_number"][6:])
    elif len(data["id_number"]) == 8:
        data["id_number"] = (data["id_number"][:2] +
                             "." +
                             data["id_number"][2:5] +
                             "." +
                             data["id_number"][5:])
    elif len(data["id_number"]) == 7:
        data["id_number"] = (data["id_number"][:1] +
                             "." +
                             data["id_number"][1:4] +
                             "." +
                             data["id_number"][4:])

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
                        z.extract(
                            model,
                            target_path
                        )

                        try:
                            # Abrir las certificaciones e ingresar los datos
                            doc = Document(target_path / model)

                            for p in doc.paragraphs:
                                for run in p.runs:
                                    if run.element.xpath("./w:drawing"):
                                        continue
                                    if "LONG_DATE" in run.text:
                                        run.text = run.text.replace(
                                            "LONG_DATE",
                                            (f"{today_date.day} de "
                                             f"{month_names[
                                                 today_date.month
                                                ]
                                                } "
                                             f"de {today_date.year}"),
                                        )
                                    if "IMPORTANT_DAYS" in run.text:
                                        run.text = run.text.replace(
                                            "IMPORTANT_DAYS",
                                            (f"{year_diffs[
                                                'INDEPENDENCE'
                                                ]
                                                }°, "
                                             f"{year_diffs[
                                                 'FEDERATION'
                                                ]
                                                }° y "
                                             f"{year_diffs[
                                                 'REVOLUTION'
                                                ]
                                                }°"
                                            ),
                                        )
                                    if "YEAR" in run.text:
                                        run.text = run.text.replace(
                                            "YEAR",
                                            str(today_date.year),
                                        )
                                    if "MONTH" in run.text:
                                        run.text = run.text.replace(
                                            "MONTH",
                                            month_names[today_date.month],
                                        )
                                    if "DAY" in run.text:
                                        run.text = run.text.replace(
                                            "DAY",
                                            str(today_date.day),
                                        )
                                    if "IMP_NAME" in run.text:
                                        run.text = run.text.replace(
                                            "IMP_NAME",
                                            data["name"],
                                        )
                                    if "IMP_CDI" in run.text:
                                        run.text = run.text.replace(
                                            "IMP_CDI",
                                            data["id_number"],
                                        )
                                    if "OFFICE_NUM" in run.text:
                                        run.text = run.text.replace(
                                            "OFFICE_NUM",
                                            data["office_no"],
                                        )
                                    if "OPEN_DATE" in run.text:
                                        run.text = run.text.replace(
                                            "OPEN_DATE",
                                            data["open_date"],
                                        )
                                doc.save(target_path / model)
                        except Exception as e:
                            messagebox.showerror(
                                "Error",
                                f"Error al procesar el documento {model}: {e}",
                            )
                            return False

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