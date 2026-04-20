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
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes")

# ------------------ INTERFÍCIE ------------------
finestra = tk.Tk()
finestra.title("Login Hospital")

tk.Label(finestra, text="Usuari").pack()
entrada_usuari = tk.Entry(finestra)
entrada_usuari.pack()

tk.Label(finestra, text="Contrasenya").pack()
entrada_contrasenya = tk.Entry(finestra, show="*")
entrada_contrasenya.pack()

tk.Button(finestra, text="Registrar", command=registrar).pack(pady=5)
tk.Button(finestra, text="Iniciar sessió", command=login).pack(pady=5)

finestra.mainloop()

