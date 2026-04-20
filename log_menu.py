id="im8k2l"
import tkinter as tk
from tkinter import messagebox
import psycopg2
import hashlib
import json
import os

# ------------------ CONFIGURACIÓ BD ------------------
def connectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="hospital",
            user="postgres",
            password="1234"
        )
        return conn
    except:
        messagebox.showerror("Error", "No s'ha pogut connectar a la BD")
        return None

# ------------------ SEGURETAT ------------------
def hash_contrasenya(contrasenya):
    return hashlib.sha256(contrasenya.encode()).hexdigest()

# ------------------ FITXER USUARIS ------------------
FITXER = "usuaris.json"

def carregar_usuaris():
    if not os.path.exists(FITXER):
        return {}
    with open(FITXER, "r") as f:
        return json.load(f)

def guardar_usuaris(dades):
    with open(FITXER, "w") as f:
        json.dump(dades, f)

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

# ------------------ REGISTRE ------------------
def registrar():
    usuari = entrada_usuari.get()
    contrasenya = entrada_contrasenya.get()

    if not usuari or not contrasenya:
        messagebox.showwarning("Avís", "Camps buits")
        return

    usuaris = carregar_usuaris()

    if usuari in usuaris:
        messagebox.showerror("Error", "L'usuari ja existeix")
        return

    usuaris[usuari] = hash_contrasenya(contrasenya)
    guardar_usuaris(usuaris)

    messagebox.showinfo("Correcte", "Usuari registrat correctament")

# ------------------ LOGIN ------------------
def login():
    usuari = entrada_usuari.get()
    contrasenya = entrada_contrasenya.get()

    usuaris = carregar_usuaris()

    if usuari in usuaris and usuaris[usuari] == hash_contrasenya(contrasenya):
        messagebox.showinfo("Correcte", "Login correcte")
        finestra.destroy()
        obrir_menu()
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes")

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

# import tkinter as tk
# from tkinter import messagebox
# import psycopg2
# import hashlib

# # ------------------ CONNEXIÓ BD ------------------
# def connectar_bd():
#     try:
#         conn = psycopg2.connect(
#             host="IP_DE_LA_TEVA_VM",   # canvia això
#             database="hospital",
#             user="postgres",
#             password="1234"
#         )
#         return conn
#     except Exception as e:
#         messagebox.showerror("Error BD", str(e))
#         return None

# # ------------------ SEGURETAT ------------------
# def hash_contrasenya(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # ------------------ REGISTRE ------------------
# def registrar():
#     usuari = entry_user.get()
#     password = entry_pass.get()

#     if not usuari or not password:
#         messagebox.showwarning("Avís", "Camps buits")
#         return

#     conn = connectar_bd()
#     if not conn:
#         return

#     try:
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM usuaris WHERE usuari=%s", (usuari,))
#         if cur.fetchone():
#             messagebox.showerror("Error", "Usuari ja existeix")
#             return

#         cur.execute(
#             "INSERT INTO usuaris (usuari, contrasenya) VALUES (%s, %s)",
#             (usuari, hash_contrasenya(password))
#         )

#         conn.commit()
#         messagebox.showinfo("OK", "Usuari registrat")

#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#     finally:
#         conn.close()

# # ------------------ LOGIN ------------------
# def login():
#     usuari = entry_user.get()
#     password = entry_pass.get()

#     conn = connectar_bd()
#     if not conn:
#         return

#     try:
#         cur = conn.cursor()

#         cur.execute(
#             "SELECT contrasenya FROM usuaris WHERE usuari=%s",
#             (usuari,)
#         )

#         result = cur.fetchone()

#         if result and result[0] == hash_contrasenya(password):
#             messagebox.showinfo("OK", "Login correcte")

#             # 🔥 GUARDAR LOG DE LOGIN
#             cur.execute(
#                 "INSERT INTO logs_login (usuari) VALUES (%s)",
#                 (usuari,)
#             )
#             conn.commit()

#         else:
#             messagebox.showerror("Error", "Credencials incorrectes")

#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#     finally:
#         conn.close()

# # ------------------ INTERFÍCIE ------------------
# finestra = tk.Tk()
# finestra.title("Sistema Hospital")
# finestra.geometry("300x250")
# finestra.configure(bg="#d9f2ff")  # 🎨 color de fons

# # Colors
# estil_label = {"bg": "#d9f2ff", "font": ("Arial", 10)}
# estil_btn = {"bg": "#4da6ff", "fg": "white", "width": 20}

# tk.Label(finestra, text="Usuari", **estil_label).pack(pady=5)
# entry_user = tk.Entry(finestra)
# entry_user.pack()

# tk.Label(finestra, text="Contrasenya", **estil_label).pack(pady=5)
# entry_pass = tk.Entry(finestra, show="*")
# entry_pass.pack()

# tk.Button(finestra, text="Registrar", command=registrar, **estil_btn).pack(pady=5)
# tk.Button(finestra, text="Login", command=login, **estil_btn).pack(pady=5)

# finestra.mainloop()
