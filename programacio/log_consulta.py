import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import hashlib
from manteniment import obrir_manteniment
from exportacio import obrir_exportacio

# ------------------ CONFIGURACIÓ BD ------------------

def connectar_bd():
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

# ------------------ SEGURETAT ------------------

def hash_contrasenya(contrasenya):
    return hashlib.sha256(contrasenya.encode()).hexdigest()

# ------------------ REGISTRE ------------------

def registrar():
    usuari = entrada_usuari.get()
    contrasenya = entrada_contrasenya.get()

    if not usuari or not contrasenya:
        messagebox.showwarning("Avís", "Camps buits")
        return

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT usuari FROM usuaris WHERE usuari = %s", (usuari,))
        if cur.fetchone():
            messagebox.showerror("Error", "L'usuari ja existeix")
        else:
            cur.execute(
                "INSERT INTO usuaris (usuari, contrasenya) VALUES (%s, %s)",
                (usuari, hash_contrasenya(contrasenya))
            )
            conn.commit()
            messagebox.showinfo("Correcte", "Usuari registrat correctament")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error BD", str(e))

# ------------------ LOGIN ------------------

def login():
    usuari = entrada_usuari.get()
    contrasenya = entrada_contrasenya.get()

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT contrasenya FROM usuaris WHERE usuari = %s", (usuari,))
        resultat = cur.fetchone()
        cur.close()
        conn.close()

        if resultat and resultat[0] == hash_contrasenya(contrasenya):
            messagebox.showinfo("Correcte", "Login correcte")
            finestra.destroy()
            obrir_menu()
        else:
            messagebox.showerror("Error", "Usuari o contrasenya incorrectes")
    except Exception as e:
        messagebox.showerror("Error BD", str(e))

# ------------------ MENÚ PRINCIPAL ------------------

def obrir_menu():
    menu = tk.Toplevel()
    menu.title("Menú Hospital")
    menu.geometry("350x400")
    menu.configure(bg="#2c3e50")

    tk.Label(menu, text="MENÚ PRINCIPAL",
             bg="#2c3e50", fg="white",
             font=("Arial", 16, "bold")).pack(pady=20)

    # tk.Button(menu, text="Pacients",
    #           bg="#1abc9c", fg="white",
    #           width=20).pack(pady=5)

    # tk.Button(menu, text="Metges",
    #           bg="#3498db", fg="white",
    #           width=20).pack(pady=5)

    # tk.Button(menu, text="Infermeria",
    #           bg="#9b59b6", fg="white",
    #           width=20).pack(pady=5)

    # Botó nou de consultes
    tk.Button(menu, text="Consultes i Informes",
              bg="#e67e22", fg="white",
              width=20,
              command=obrir_consultes).pack(pady=5)
    
    tk.Button(menu, text="Manteniment",
          bg="#1abc9c", fg="white", width=20,
          command=obrir_manteniment).pack(pady=5)
    
    tk.Button(menu, text="Exportació de Dades",
          bg="#2980b9", fg="white", width=20,
          command=obrir_exportacio).pack(pady=5)

    tk.Button(menu, text="Sortir",
              bg="#e74c3c", fg="white",
              width=20,
              command=menu.destroy).pack(pady=20)

# ------------------ BLOC DE CONSULTES ------------------

def obrir_consultes():
    """Obre la pantalla principal de consultes i informes"""
    consultes = tk.Toplevel()
    consultes.title("Consultes i Informes")
    consultes.geometry("400x350")
    consultes.configure(bg="#2c3e50")

    tk.Label(consultes, text="CONSULTES I INFORMES",
             bg="#2c3e50", fg="white",
             font=("Arial", 14, "bold")).pack(pady=20)

    # Obligatori 1: Informe per planta
    tk.Button(consultes, text="Informe per Planta",
              bg="#1abc9c", fg="white", width=30,
              command=consulta_planta).pack(pady=8)

    # Obligatori 2: Tot el personal
    tk.Button(consultes, text="Informe de Personal",
              bg="#3498db", fg="white", width=30,
              command=consulta_personal).pack(pady=8)

    # Obligatori 3: Visites per dia
    tk.Button(consultes, text="Visites per Dia",
              bg="#9b59b6", fg="white", width=30,
              command=consulta_visites_dia).pack(pady=8)

    # Opcional: Ranking metges
    tk.Button(consultes, text="Ranking de Metges",
              bg="#e67e22", fg="white", width=30,
              command=consulta_ranking_metges).pack(pady=8)

    tk.Button(consultes, text="Tancar",
              bg="#e74c3c", fg="white", width=30,
              command=consultes.destroy).pack(pady=10)


# ------------------ CONSULTA 1: INFORME PER PLANTA ------------------

def consulta_planta():
    """Donada una planta, mostra habitacions, quiròfans i infermeria"""
    finestra_planta = tk.Toplevel()
    finestra_planta.title("Informe per Planta")
    finestra_planta.geometry("600x450")
    finestra_planta.configure(bg="#2c3e50")

    tk.Label(finestra_planta, text="Informe per Planta",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camp per introduir el número de planta
    frame_input = tk.Frame(finestra_planta, bg="#2c3e50")
    frame_input.pack(pady=5)

    tk.Label(frame_input, text="Número de planta (1-4):",
             bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)

    entrada_planta = tk.Entry(frame_input, width=5)
    entrada_planta.grid(row=0, column=1, padx=5)

    # Taula de resultats
    frame_taula = tk.Frame(finestra_planta)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("Element", "Quantitat")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=8)
    for col in columnes:
        taula.heading(col, text=col)
        taula.column(col, width=200, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def cercar():
        # Netegem la taula
        for row in taula.get_children():
            taula.delete(row)

        num_planta = entrada_planta.get()
        if not num_planta.isdigit():
            messagebox.showwarning("Avís", "Introdueix un número de planta vàlid")
            return

        conn = connectar_bd()
        if conn is None:
            return

        try:
            cur = conn.cursor()

            # Número d'habitacions
            cur.execute("""
                SELECT COUNT(*) FROM Habitacio
                WHERE num_planta = %s
            """, (num_planta,))
            habitacions = cur.fetchone()[0]

            # Número de quiròfans
            cur.execute("""
                SELECT COUNT(*) FROM Quirofan
                WHERE num_planta = %s
            """, (num_planta,))
            quirofans = cur.fetchone()[0]

            # Número d'infermeria a la planta
            # (infermers no assignats a cap metge = són de planta)
            cur.execute("""
                SELECT COUNT(*) FROM Infermeria i
                LEFT JOIN Assignat a ON i.id_personal = a.id_infermer
                WHERE a.id_metge IS NULL
            """)
            infermeria = cur.fetchone()[0]

            cur.close()
            conn.close()

            # Inserim resultats a la taula
            taula.insert("", "end", values=("Habitacions", habitacions))
            taula.insert("", "end", values=("Quiròfans", quirofans))
            taula.insert("", "end", values=("Personal d'Infermeria de Planta", infermeria))

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra_planta, text="Cercar",
              bg="#1abc9c", fg="white",
              command=cercar).pack(pady=5)


# ------------------ CONSULTA 2: INFORME DE PERSONAL ------------------

def consulta_personal():
    """Mostra tot el personal que treballa a l'hospital"""
    finestra_personal = tk.Toplevel()
    finestra_personal.title("Informe de Personal")
    finestra_personal.geometry("700x450")
    finestra_personal.configure(bg="#2c3e50")

    tk.Label(finestra_personal, text="Tot el Personal de l'Hospital",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Taula de resultats
    frame_taula = tk.Frame(finestra_personal)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("ID", "Nom", "Cognoms", "DNI", "Tipus", "Detall")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=15)

    amplades = [50, 100, 150, 100, 100, 150]
    for col, amp in zip(columnes, amplades):
        taula.heading(col, text=col)
        taula.column(col, width=amp, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # Metges
        cur.execute("""
            SELECT p.id_personal, p.nom, p.cognoms, p.dni,
                   'Metge' AS tipus, m.especialitat
            FROM Personal_Seguretat p
            JOIN Metges m ON p.id_personal = m.id_personal
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        # Infermeria
        cur.execute("""
            SELECT p.id_personal, p.nom, p.cognoms, p.dni,
                   'Infermer/a' AS tipus, i.titulacio
            FROM Personal_Seguretat p
            JOIN Infermeria i ON p.id_personal = i.id_personal
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        # Varis
        cur.execute("""
            SELECT p.id_personal, p.nom, p.cognoms, p.dni,
                   'Varis' AS tipus, v.tipus_feina
            FROM Personal_Seguretat p
            JOIN Varis v ON p.id_personal = v.id_personal
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error BD", str(e))


# ------------------ CONSULTA 3: VISITES PER DIA ------------------

def consulta_visites_dia():
    """Mostra el nombre de visites ateses per dia"""
    finestra_visites = tk.Toplevel()
    finestra_visites.title("Visites per Dia")
    finestra_visites.geometry("400x450")
    finestra_visites.configure(bg="#2c3e50")

    tk.Label(finestra_visites, text="Nombre de Visites per Dia",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Taula de resultats
    frame_taula = tk.Frame(finestra_visites)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("Data", "Total Visites")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=15)
    for col in columnes:
        taula.heading(col, text=col)
        taula.column(col, width=150, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT data, COUNT(*) AS total_visites
            FROM Visites
            GROUP BY data
            ORDER BY data DESC
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error BD", str(e))


# ------------------ CONSULTA 4 (OPCIONAL): RANKING METGES ------------------

def consulta_ranking_metges():
    """Ranking de metges que atenen més pacients"""
    finestra_ranking = tk.Toplevel()
    finestra_ranking.title("Ranking de Metges")
    finestra_ranking.geometry("500x450")
    finestra_ranking.configure(bg="#2c3e50")

    tk.Label(finestra_ranking, text="Ranking de Metges per Pacients Atesos",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Taula de resultats
    frame_taula = tk.Frame(finestra_ranking)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("Posició", "Nom", "Cognoms", "Especialitat", "Total Pacients")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=15)

    amplades = [60, 100, 130, 130, 100]
    for col, amp in zip(columnes, amplades):
        taula.heading(col, text=col)
        taula.column(col, width=amp, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT v.id_pacient) DESC) AS posicio,
                p.nom,
                p.cognoms,
                m.especialitat,
                COUNT(DISTINCT v.id_pacient) AS total_pacients
            FROM Metges m
            JOIN Personal p ON m.id_personal = p.id_personal
            JOIN Visites v ON m.id_personal = v.id_metge
            GROUP BY m.id_personal, p.nom, p.cognoms, m.especialitat
            ORDER BY total_pacients DESC
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error BD", str(e))


# ------------------ INTERFÍCIE LOGIN ------------------

finestra = tk.Tk()
finestra.title("Login Hospital")
finestra.geometry("300x250")
finestra.configure(bg="#34495e")

tk.Label(finestra, text="Usuari",
         bg="#34495e", fg="white",
         font=("Arial", 10)).pack()

entrada_usuari = tk.Entry(finestra)
entrada_usuari.pack()

tk.Label(finestra, text="Contrasenya",
         bg="#34495e", fg="white",
         font=("Arial", 10)).pack()

entrada_contrasenya = tk.Entry(finestra, show="*")
entrada_contrasenya.pack()

tk.Button(finestra, text="Registrar",
          bg="#3498db", fg="white",
          width=15,
          command=registrar).pack(pady=5)

tk.Button(finestra, text="Iniciar sessió",
          bg="#2ecc71", fg="white",
          width=15,
          command=login).pack(pady=5)

finestra.mainloop()
