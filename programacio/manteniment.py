import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from datetime import date
from manteniment_extra import infermeria_per_metge, operacions_per_dia, visites_per_dia

# ------------------ CONFIGURACIÓ BD ------------------

def connectar_bd():
    """Connecta a la base de dades PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="192.168.250.3",
            database="hospital",
            user="postgres",
            password="123456"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut connectar a la BD:\n{e}")
        return None


# ======================================================
# MENÚ PRINCIPAL DE MANTENIMENT
# ======================================================

def obrir_manteniment():
    """Obre la pantalla principal del bloc de manteniment"""
    menu = tk.Toplevel()
    menu.title("Manteniment")
    menu.geometry("400x500")
    menu.configure(bg="#2c3e50")

    tk.Label(menu, text="MANTENIMENT",
             bg="#2c3e50", fg="white",
             font=("Arial", 16, "bold")).pack(pady=20)

    # Pacients
    tk.Button(menu, text="Alta Pacient",
              bg="#1abc9c", fg="white", width=25,
              command=alta_pacient).pack(pady=5)

    tk.Button(menu, text="Baixa Pacient",
              bg="#e74c3c", fg="white", width=25,
              command=baixa_pacient).pack(pady=5)

    # Personal
    tk.Button(menu, text="Alta Personal",
              bg="#3498db", fg="white", width=25,
              command=alta_personal).pack(pady=5)

    tk.Button(menu, text="Baixa Personal",
              bg="#e74c3c", fg="white", width=25,
              command=baixa_personal).pack(pady=5)

    # Visites
    tk.Button(menu, text="Alta Visita",
              bg="#9b59b6", fg="white", width=25,
              command=alta_visita).pack(pady=5)

    tk.Button(menu, text="Baixa Visita",
              bg="#e74c3c", fg="white", width=25,
              command=baixa_visita).pack(pady=5)

    # Operacions
    tk.Button(menu, text="Alta Operació",
              bg="#e67e22", fg="white", width=25,
              command=alta_operacio).pack(pady=5)

    tk.Button(menu, text="Baixa Operació",
              bg="#e74c3c", fg="white", width=25,
              command=baixa_operacio).pack(pady=5)

    # Reserves habitació
    tk.Button(menu, text="Alta Reserva Habitació",
              bg="#16a085", fg="white", width=25,
              command=alta_reserva).pack(pady=5)

    tk.Button(menu, text="Baixa Reserva Habitació",
              bg="#e74c3c", fg="white", width=25,
              command=baixa_reserva).pack(pady=5)
    
    tk.Button(menu, text="Infermeria per Metge o Planta",
          bg="#2980b9", fg="white", width=25,
          command=infermeria_per_metge).pack(pady=5)

    tk.Button(menu, text="Operacions per Dia i Quiròfan",
          bg="#2980b9", fg="white", width=25,
          command=operacions_per_dia).pack(pady=5)

    tk.Button(menu, text="Visites Planificades per Dia",
          bg="#2980b9", fg="white", width=25,
          command=visites_per_dia).pack(pady=5)
    

    tk.Button(menu, text="Tancar",
              bg="#7f8c8d", fg="white", width=25,
              command=menu.destroy).pack(pady=20)


# ======================================================
# PACIENTS
# ======================================================

def alta_pacient():
    """Formulari per donar d'alta un nou pacient. Crida alta_pacient() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Alta Pacient")
    finestra.geometry("350x350")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Alta Pacient", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camps del formulari
    camps = [("ID Pacient", "id"), ("Nom", "nom"), ("Cognoms", "cognoms"),
             ("Data Naixement (YYYY-MM-DD)", "data"), ("Telèfon", "telefon")]
    entrades = {}

    for label, clau in camps:
        tk.Label(finestra, text=label, bg="#2c3e50", fg="white").pack()
        entrada = tk.Entry(finestra, width=30)
        entrada.pack(pady=2)
        entrades[clau] = entrada

    def guardar():
        """Crida la funció alta_pacient() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            # Crida a la funció SQL alta_pacient
            cur.execute(
                "SELECT alta_pacient(%s, %s, %s, %s, %s)",
                (
                    entrades["id"].get(),
                    entrades["nom"].get(),
                    entrades["cognoms"].get(),
                    entrades["data"].get(),
                    entrades["telefon"].get()
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Pacient donat d'alta correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Guardar", bg="#1abc9c", fg="white",
              command=guardar).pack(pady=10)


def baixa_pacient():
    """Formulari per donar de baixa un pacient. Crida baixa_pacient() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Baixa Pacient")
    finestra.geometry("300x200")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Baixa Pacient", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(finestra, text="ID Pacient", bg="#2c3e50", fg="white").pack()
    entrada_id = tk.Entry(finestra, width=20)
    entrada_id.pack(pady=5)

    def eliminar():
        """Crida la funció baixa_pacient() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            # Crida a la funció SQL baixa_pacient
            cur.execute("SELECT baixa_pacient(%s)", (entrada_id.get(),))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Pacient donat de baixa correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Eliminar", bg="#e74c3c", fg="white",
              command=eliminar).pack(pady=10)


# ======================================================
# PERSONAL
# ======================================================

def alta_personal():
    """Formulari per donar d'alta personal. Crida alta_personal() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Alta Personal")
    finestra.geometry("400x500")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Alta Personal", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camps bàsics de personal
    camps = [("ID Personal", "id"), ("Nom", "nom"), ("Cognoms", "cognoms"),
             ("DNI", "dni"), ("Adreça", "adreca"), ("Telèfon", "telefon")]
    entrades = {}

    for label, clau in camps:
        tk.Label(finestra, text=label, bg="#2c3e50", fg="white").pack()
        entrada = tk.Entry(finestra, width=30)
        entrada.pack(pady=2)
        entrades[clau] = entrada

    # Selector de tipus de personal
    tk.Label(finestra, text="Tipus de Personal", bg="#2c3e50", fg="white").pack()
    tipus_var = tk.StringVar(value="metge")
    frame_tipus = tk.Frame(finestra, bg="#2c3e50")
    frame_tipus.pack()
    for text, val in [("Metge", "metge"), ("Infermer/a", "infermer"), ("Varis", "varis")]:
        tk.Radiobutton(frame_tipus, text=text, variable=tipus_var, value=val,
                       bg="#2c3e50", fg="white", selectcolor="#1a252f").pack(side="left", padx=5)

    def guardar():
        """Crida alta_personal() i després insereix a la subtaula corresponent"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()

            # Crida a la funció SQL alta_personal (insereix a Personal)
            cur.execute(
                "SELECT alta_personal(%s, %s, %s, %s, %s, %s)",
                (
                    entrades["id"].get(),
                    entrades["nom"].get(),
                    entrades["cognoms"].get(),
                    entrades["dni"].get(),
                    entrades["adreca"].get(),
                    entrades["telefon"].get()
                )
            )

            # Insereix a la subtaula segons el tipus escollit
            tipus = tipus_var.get()
            id_personal = entrades["id"].get()

            if tipus == "metge":
                cur.execute(
                    "INSERT INTO Metges (id_personal, especialitat, estudis, curriculum) VALUES (%s, %s, %s, %s)",
                    (id_personal, "Pendent", "Pendent", "Pendent")
                )
            elif tipus == "infermer":
                cur.execute(
                    "INSERT INTO Infermeria (id_personal, titulacio, experiencia) VALUES (%s, %s, %s)",
                    (id_personal, "Pendent", 0)
                )
            elif tipus == "varis":
                cur.execute(
                    "INSERT INTO Varis (id_personal, tipus_feina) VALUES (%s, %s)",
                    (id_personal, "Pendent")
                )

            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Personal donat d'alta correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Guardar", bg="#3498db", fg="white",
              command=guardar).pack(pady=10)


def baixa_personal():
    """Formulari per donar de baixa personal. Crida baixa_personal() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Baixa Personal")
    finestra.geometry("300x200")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Baixa Personal", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(finestra, text="ID Personal", bg="#2c3e50", fg="white").pack()
    entrada_id = tk.Entry(finestra, width=20)
    entrada_id.pack(pady=5)

    def eliminar():
        """Crida la funció baixa_personal() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            # Crida a la funció SQL baixa_personal
            cur.execute("SELECT baixa_personal(%s)", (entrada_id.get(),))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Personal donat de baixa correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Eliminar", bg="#e74c3c", fg="white",
              command=eliminar).pack(pady=10)


# ======================================================
# VISITES
# ======================================================

def alta_visita():
    """Formulari per donar d'alta una visita. Crida alta_visita() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Alta Visita")
    finestra.geometry("350x380")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Alta Visita", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    camps = [("ID Visita", "id"), ("Data (YYYY-MM-DD)", "data"),
             ("Hora (HH:MM)", "hora"), ("Diagnòstic", "diagnostic"),
             ("ID Pacient", "pacient"), ("ID Metge", "metge")]
    entrades = {}

    for label, clau in camps:
        tk.Label(finestra, text=label, bg="#2c3e50", fg="white").pack()
        entrada = tk.Entry(finestra, width=30)
        entrada.pack(pady=2)
        entrades[clau] = entrada

    def guardar():
        """Crida la funció alta_visita() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            # Crida a la funció SQL alta_visita
            cur.execute(
                "SELECT alta_visita(%s, %s, %s, %s, %s, %s)",
                (
                    entrades["id"].get(),
                    entrades["data"].get(),
                    entrades["hora"].get(),
                    entrades["diagnostic"].get(),
                    entrades["pacient"].get(),
                    entrades["metge"].get()
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Visita donada d'alta correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Guardar", bg="#9b59b6", fg="white",
              command=guardar).pack(pady=10)


def baixa_visita():
    """Formulari per donar de baixa una visita. Crida baixa_visita() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Baixa Visita")
    finestra.geometry("300x200")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Baixa Visita", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(finestra, text="ID Visita", bg="#2c3e50", fg="white").pack()
    entrada_id = tk.Entry(finestra, width=20)
    entrada_id.pack(pady=5)

    def eliminar():
        """Crida la funció baixa_visita() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT baixa_visita(%s)", (entrada_id.get(),))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Visita donada de baixa correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Eliminar", bg="#e74c3c", fg="white",
              command=eliminar).pack(pady=10)


# ======================================================
# OPERACIONS
# ======================================================

def alta_operacio():
    """Formulari per donar d'alta una operació. Crida alta_operacio() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Alta Operació")
    finestra.geometry("350x300")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Alta Operació", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    camps = [("ID Operació", "id"), ("Data (YYYY-MM-DD)", "data"),
             ("Hora (HH:MM)", "hora"), ("Núm. Quiròfan", "quirofan")]
    entrades = {}

    for label, clau in camps:
        tk.Label(finestra, text=label, bg="#2c3e50", fg="white").pack()
        entrada = tk.Entry(finestra, width=30)
        entrada.pack(pady=2)
        entrades[clau] = entrada

    def guardar():
        """Crida la funció alta_operacio() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT alta_operacio(%s, %s, %s, %s)",
                (
                    entrades["id"].get(),
                    entrades["data"].get(),
                    entrades["hora"].get(),
                    entrades["quirofan"].get()
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Operació donada d'alta correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Guardar", bg="#e67e22", fg="white",
              command=guardar).pack(pady=10)


def baixa_operacio():
    """Formulari per donar de baixa una operació. Crida baixa_operacio() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Baixa Operació")
    finestra.geometry("300x200")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Baixa Operació", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(finestra, text="ID Operació", bg="#2c3e50", fg="white").pack()
    entrada_id = tk.Entry(finestra, width=20)
    entrada_id.pack(pady=5)

    def eliminar():
        """Crida la funció baixa_operacio() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT baixa_operacio(%s)", (entrada_id.get(),))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Operació donada de baixa correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Eliminar", bg="#e74c3c", fg="white",
              command=eliminar).pack(pady=10)


# ======================================================
# RESERVES HABITACIÓ
# ======================================================

def alta_reserva():
    """Formulari per donar d'alta una reserva. Crida alta_reserva() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Alta Reserva Habitació")
    finestra.geometry("350x300")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Alta Reserva Habitació", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    camps = [("ID Pacient", "pacient"), ("Núm. Habitació", "habitacio"),
             ("Data Ingrés (YYYY-MM-DD)", "ingres"),
             ("Data Sortida Prevista (YYYY-MM-DD)", "sortida")]
    entrades = {}

    for label, clau in camps:
        tk.Label(finestra, text=label, bg="#2c3e50", fg="white").pack()
        entrada = tk.Entry(finestra, width=30)
        entrada.pack(pady=2)
        entrades[clau] = entrada

    def guardar():
        """Crida la funció alta_reserva() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT alta_reserva(%s, %s, %s, %s)",
                (
                    entrades["pacient"].get(),
                    entrades["habitacio"].get(),
                    entrades["ingres"].get(),
                    entrades["sortida"].get()
                )
            )
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Reserva donada d'alta correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Guardar", bg="#16a085", fg="white",
              command=guardar).pack(pady=10)


def baixa_reserva():
    """Formulari per donar de baixa una reserva. Crida baixa_reserva() de PostgreSQL"""
    finestra = tk.Toplevel()
    finestra.title("Baixa Reserva Habitació")
    finestra.geometry("300x220")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Baixa Reserva Habitació", bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(finestra, text="ID Pacient", bg="#2c3e50", fg="white").pack()
    entrada_pacient = tk.Entry(finestra, width=20)
    entrada_pacient.pack(pady=5)

    tk.Label(finestra, text="Núm. Habitació", bg="#2c3e50", fg="white").pack()
    entrada_habitacio = tk.Entry(finestra, width=20)
    entrada_habitacio.pack(pady=5)

    def eliminar():
        """Crida la funció baixa_reserva() de PostgreSQL"""
        conn = connectar_bd()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT baixa_reserva(%s, %s)",
                (entrada_pacient.get(), entrada_habitacio.get())
            )
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Correcte", "Reserva donada de baixa correctament")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Eliminar", bg="#e74c3c", fg="white",
              command=eliminar).pack(pady=10)