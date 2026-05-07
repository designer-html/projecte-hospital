import tkinter as tk
from tkinter import messagebox
import psycopg2
import hashlib

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

# ------------------ REGISTRE (POSTGRESQL) ------------------

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

        # comprobar si existe
        cur.execute("SELECT usuari FROM usuaris WHERE usuari = %s", (usuari,))
        if cur.fetchone():
            messagebox.showerror("Error", "L'usuari ja existeix")
        else:
            # insertar usuario
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

# ------------------ LOGIN (POSTGRESQL) ------------------

def login():
    usuari = entrada_usuari.get()
    contrasenya = entrada_contrasenya.get()

    conn = connectar_bd()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT contrasenya FROM usuaris WHERE usuari = %s",
            (usuari,)
        )

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

# ------------------ MENÚ ------------------

def obrir_menu():
    menu = tk.Toplevel()
    menu.title("Menú Hospital")
    menu.geometry("350x350")
    menu.configure(bg="#2c3e50")

    tk.Label(menu, text="MENÚ PRINCIPAL",
             bg="#2c3e50", fg="white",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(menu, text="Pacients",
              bg="#1abc9c", fg="white",
              width=20).pack(pady=5)

    tk.Button(menu, text="Metges",
              bg="#3498db", fg="white",
              width=20).pack(pady=5)

    tk.Button(menu, text="Infermeria",
              bg="#9b59b6", fg="white",
              width=20).pack(pady=5)

    tk.Button(menu, text="Sortir",
              bg="#e74c3c", fg="white",
              width=20,
              command=menu.destroy).pack(pady=20)

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
