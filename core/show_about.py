import tkinter as tk

def show_about(self, parent):
    """
    Crea una ventana secundaria con la información del software.
    """
    about_win = tk.Toplevel(parent)
    about_win.title("Acerca de KODIAK")
    about_win.geometry("350x280")
    about_win.resizable(False, False)
    
    # Bloquear interacción con la ventana principal
    about_win.grab_set()

    # Configurar pesos
    about_win.columnconfigure(0, weight=1)

    # Título
    tk.Label(
        about_win, 
        text="KODIAK", 
        font=(
            "Helvetica",
            16,
            "bold",
        ),
    ).grid(
        row=0,
        column=0,
        pady=(
            20,
            10,
        ),
        sticky="n",
    )
    
    # Descripción y Versión
    tk.Label(
        about_win, 
        text="Versión 1.1.4\nSistema de Gestión de Labores Sociales",
        font=(
            "Helvetica",
            10,
        ),
        justify="center",
    ).grid(
        row=1,
        column=0,
        pady=5,
        sticky="n",
    )

    # Créditos
    tk.Label(
        about_win, 
        text="Desarrollado por:\nThe Thartarus",
        font=(
            "Helvetica",
            10,
            "italic",
        ),
        fg="blue",
    ).grid(
        row=2,
        column=0,
        pady=15,
        sticky="n",
    )

    # Copyright
    tk.Label(
        about_win, 
        text="© 2026 - Todos los derechos reservados",
        font=(
            "Helvetica",
            8,
        )
    ).grid(
        row=3,
        column=0,
        pady=5,
        sticky="n",
    )

    # Cerrar
    tk.Button(
        about_win, 
        text="Cerrar", 
        width=12,
        command=about_win.destroy
    ).grid(
        row=4,
        column=0,
        pady=20,
        sticky="n",
    )