import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

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
# 1. INFERMERIA PER METGE O PLANTA (OBLIGATORI)
# ======================================================

def infermeria_per_metge():
    """Mostra si cada infermer/a depèn d'un metge o és de planta"""
    finestra = tk.Toplevel()
    finestra.title("Infermeria per Metge o Planta")
    finestra.geometry("650x400")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Infermeria — Assignació per Metge o Planta",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    frame_taula = tk.Frame(finestra)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("ID", "Nom", "Cognoms", "Titulació", "Assignació")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=12)

    amplades = [50, 100, 150, 150, 180]
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
        # Mostra cada infermer/a i si està assignat a un metge o és de planta
        cur.execute("""
            SELECT
                p.id_personal,
                p.nom,
                p.cognoms,
                i.titulacio,
                CASE
                    WHEN a.id_metge IS NOT NULL
                        THEN 'Metge: ' || pm.nom || ' ' || pm.cognoms
                    ELSE 'De Planta'
                END AS assignacio
            FROM Infermeria i
            JOIN Personal p ON i.id_personal = p.id_personal
            LEFT JOIN Assignat a ON i.id_personal = a.id_infermer
            LEFT JOIN Personal pm ON a.id_metge = pm.id_personal
            ORDER BY assignacio, p.cognoms
        """)
        for row in cur.fetchall():
            taula.insert("", "end", values=row)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error BD", str(e))


# ======================================================
# 2. OPERACIONS PER DIA I QUIRÒFAN (OBLIGATORI)
# ======================================================

def operacions_per_dia():
    """Mostra les operacions previstes per un dia i quiròfan concret"""
    finestra = tk.Toplevel()
    finestra.title("Operacions per Dia i Quiròfan")
    finestra.geometry("750x450")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Operacions per Dia i Quiròfan",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camps de cerca
    frame_input = tk.Frame(finestra, bg="#2c3e50")
    frame_input.pack(pady=5)

    tk.Label(frame_input, text="Data (YYYY-MM-DD):",
             bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)
    entrada_data = tk.Entry(frame_input, width=15)
    entrada_data.grid(row=0, column=1, padx=5)

    tk.Label(frame_input, text="Núm. Quiròfan:",
             bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)
    entrada_quirofan = tk.Entry(frame_input, width=8)
    entrada_quirofan.grid(row=0, column=3, padx=5)

    # Taula de resultats
    frame_taula = tk.Frame(finestra)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("ID Op.", "Hora", "Pacient", "Metge", "Infermeria")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=12)

    amplades = [60, 70, 150, 150, 200]
    for col, amp in zip(columnes, amplades):
        taula.heading(col, text=col)
        taula.column(col, width=amp, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def cercar():
        """Consulta les operacions del dia i quiròfan indicats"""
        for row in taula.get_children():
            taula.delete(row)

        conn = connectar_bd()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    o.id_operacio,
                    o.hora,
                    COALESCE(
                        (SELECT pp.nom || ' ' || pp.cognoms
                         FROM Fa f
                         JOIN Personal pp ON f.id_metge = pp.id_personal
                         WHERE f.id_operacio = o.id_operacio
                         LIMIT 1),
                        'Sense metge assignat'
                    ) AS metge,
                    COALESCE(
                        (SELECT pac.nom || ' ' || pac.cognoms
                         FROM Reserva_Quirofan rq
                         JOIN Pacients pac ON rq.id_pacient = pac.id_pacient
                         WHERE rq.num_quirofan = o.num_quirofan
                           AND rq.data = o.data
                           AND rq.hora = o.hora
                         LIMIT 1),
                        'Sense pacient assignat'
                    ) AS pacient,
                    COALESCE(
                        (SELECT STRING_AGG(pi.nom || ' ' || pi.cognoms, ', ')
                         FROM Assistencia ass
                         JOIN Personal pi ON ass.id_infermer = pi.id_personal
                         WHERE ass.id_operacio = o.id_operacio),
                        'Sense infermeria'
                    ) AS infermeria
                FROM Operacions o
                WHERE o.data = %s AND o.num_quirofan = %s
                ORDER BY o.hora
            """, (entrada_data.get(), entrada_quirofan.get()))

            files = cur.fetchall()
            cur.close()
            conn.close()

            if not files:
                messagebox.showinfo("Info", "No hi ha operacions per aquest dia i quiròfan")
                return

            for row in files:
                taula.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Cercar", bg="#e67e22", fg="white",
              command=cercar).pack(pady=5)


# ======================================================
# 3. VISITES PLANIFICADES PER DIA (OBLIGATORI)
# ======================================================

def visites_per_dia():
    """Mostra les visites planificades per un dia concret"""
    finestra = tk.Toplevel()
    finestra.title("Visites per Dia")
    finestra.geometry("650x420")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Visites Planificades per Dia",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camp de cerca
    frame_input = tk.Frame(finestra, bg="#2c3e50")
    frame_input.pack(pady=5)

    tk.Label(frame_input, text="Data (YYYY-MM-DD):",
             bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)
    entrada_data = tk.Entry(frame_input, width=15)
    entrada_data.grid(row=0, column=1, padx=5)

    # Taula de resultats
    frame_taula = tk.Frame(finestra)
    frame_taula.pack(pady=10, fill="both", expand=True, padx=10)

    columnes = ("ID Visita", "Hora", "Pacient", "Metge", "Diagnòstic")
    taula = ttk.Treeview(frame_taula, columns=columnes, show="headings", height=12)

    amplades = [70, 70, 150, 150, 180]
    for col, amp in zip(columnes, amplades):
        taula.heading(col, text=col)
        taula.column(col, width=amp, anchor="center")

    scrollbar = ttk.Scrollbar(frame_taula, orient="vertical", command=taula.yview)
    taula.configure(yscrollcommand=scrollbar.set)
    taula.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def cercar():
        """Consulta les visites del dia indicat"""
        for row in taula.get_children():
            taula.delete(row)

        conn = connectar_bd()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    v.id_visita,
                    v.hora,
                    pp.nom || ' ' || pp.cognoms AS pacient,
                    pm.nom || ' ' || pm.cognoms AS metge,
                    v.diagnostic
                FROM Visites v
                JOIN Pacients p  ON v.id_pacient = p.id_pacient
                JOIN Personal pp ON p.id_pacient = pp.id_personal
                JOIN Metges m    ON v.id_metge = m.id_personal
                JOIN Personal pm ON m.id_personal = pm.id_personal
                WHERE v.data = %s
                ORDER BY v.hora
            """, (entrada_data.get(),))

            files = cur.fetchall()
            cur.close()
            conn.close()

            if not files:
                messagebox.showinfo("Info", "No hi ha visites per aquest dia")
                return

            for row in files:
                taula.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Cercar", bg="#9b59b6", fg="white",
              command=cercar).pack(pady=5)
