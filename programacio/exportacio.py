import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import psycopg2
import json
import os
from datetime import date

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
# MENÚ PRINCIPAL D'EXPORTACIÓ
# ======================================================

def obrir_exportacio():
    """Obre la pantalla principal del bloc d'exportació"""
    finestra = tk.Toplevel()
    finestra.title("Exportació de Dades")
    finestra.geometry("400x300")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="EXPORTACIÓ DE DADES",
             bg="#2c3e50", fg="white",
             font=("Arial", 14, "bold")).pack(pady=20)

    # Exportar visites entre dues dates en JSON
    tk.Button(finestra, text="Exportar Visites a JSON",
              bg="#1abc9c", fg="white", width=28,
              command=exportar_visites_json).pack(pady=10)

    # Generar JSON Schema
    tk.Button(finestra, text="Generar JSON Schema",
              bg="#3498db", fg="white", width=28,
              command=generar_json_schema).pack(pady=10)

    tk.Button(finestra, text="Tancar",
              bg="#e74c3c", fg="white", width=28,
              command=finestra.destroy).pack(pady=20)


# ======================================================
# EXPORTAR VISITES A JSON
# ======================================================

def exportar_visites_json():
    """Exporta totes les visites entre dues dates a un fitxer JSON indentat"""
    finestra = tk.Toplevel()
    finestra.title("Exportar Visites a JSON")
    finestra.geometry("400x300")
    finestra.configure(bg="#2c3e50")

    tk.Label(finestra, text="Exportar Visites a JSON",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(pady=10)

    # Camp data inici
    tk.Label(finestra, text="Data Inici (YYYY-MM-DD):",
             bg="#2c3e50", fg="white").pack()
    entrada_inici = tk.Entry(finestra, width=20)
    entrada_inici.pack(pady=5)

    # Camp data fi
    tk.Label(finestra, text="Data Fi (YYYY-MM-DD):",
             bg="#2c3e50", fg="white").pack()
    entrada_fi = tk.Entry(finestra, width=20)
    entrada_fi.pack(pady=5)

    # Etiqueta per mostrar resultat
    label_resultat = tk.Label(finestra, text="",
                              bg="#2c3e50", fg="#2ecc71",
                              font=("Arial", 9))
    label_resultat.pack(pady=5)

    def exportar():
        """Consulta les visites i les exporta a JSON"""
        data_inici = entrada_inici.get()
        data_fi = entrada_fi.get()

        if not data_inici or not data_fi:
            messagebox.showwarning("Avís", "Introdueix les dues dates")
            return

        conn = connectar_bd()
        if conn is None:
            return

        try:
            cur = conn.cursor()

            # Consulta visites entre les dues dates amb dades del pacient i metge
            cur.execute("""
                SELECT
                    v.id_visita,
                    v.data,
                    v.hora,
                    v.diagnostic,
                    p.id_pacient,
                    p.nom        AS nom_pacient,
                    p.cognoms    AS cognoms_pacient,
                    p.data_naix,
                    p.telefon    AS telefon_pacient,
                    per.nom      AS nom_metge,
                    per.cognoms  AS cognoms_metge,
                    m.especialitat
                FROM Visites v
                JOIN Pacients p   ON v.id_pacient = p.id_pacient
                JOIN Metges m     ON v.id_metge = m.id_personal
                JOIN Personal per ON m.id_personal = per.id_personal
                WHERE v.data BETWEEN %s AND %s
                ORDER BY v.data, v.hora
            """, (data_inici, data_fi))

            files = cur.fetchall()
            cur.close()
            conn.close()

            if not files:
                messagebox.showinfo("Info", "No hi ha visites en aquest període")
                return

            # Construim l'estructura JSON
            visites = []
            for f in files:
                visita = {
                    "id_visita": f[0],
                    "data": str(f[1]),
                    "hora": str(f[2]),
                    "diagnostic": f[3],
                    "pacient": {
                        "id_pacient": f[4],
                        "nom": f[5],
                        "cognoms": f[6],
                        "data_naixement": str(f[7]),
                        "telefon": f[8]
                    },
                    "metge": {
                        "nom": f[9],
                        "cognoms": f[10],
                        "especialitat": f[11]
                    }
                }
                visites.append(visita)

            # Estructura principal del JSON
            dades = {
                "hospital": "Hospital de Blanes",
                "periode": {
                    "data_inici": data_inici,
                    "data_fi": data_fi
                },
                "total_visites": len(visites),
                "visites": visites
            }

            # Demanem on guardar el fitxer
            ruta = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialfile=f"visites_{data_inici}_{data_fi}.json"
            )

            if not ruta:
                return

            # Guardem el JSON indentat amb tabulacions
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(dades, f, ensure_ascii=False, indent=4)

            label_resultat.config(
                text=f"✓ Exportades {len(visites)} visites correctament"
            )
            messagebox.showinfo("Correcte",
                                f"Fitxer guardat a:\n{ruta}\n\n"
                                f"Total visites exportades: {len(visites)}")

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    tk.Button(finestra, text="Exportar",
              bg="#1abc9c", fg="white", width=20,
              command=exportar).pack(pady=10)


# ======================================================
# GENERAR JSON SCHEMA
# ======================================================

def generar_json_schema():
    """Genera el JSON Schema del fitxer de visites i el guarda"""

    # Definim l'esquema JSON Schema de les visites
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Visites Hospital de Blanes",
        "description": "Esquema de les visites exportades de l'Hospital de Blanes",
        "type": "object",
        "required": ["hospital", "periode", "total_visites", "visites"],
        "properties": {
            "hospital": {
                "type": "string",
                "description": "Nom de l'hospital"
            },
            "periode": {
                "type": "object",
                "required": ["data_inici", "data_fi"],
                "properties": {
                    "data_inici": {
                        "type": "string",
                        "format": "date",
                        "description": "Data d'inici del periode (YYYY-MM-DD)"
                    },
                    "data_fi": {
                        "type": "string",
                        "format": "date",
                        "description": "Data de fi del periode (YYYY-MM-DD)"
                    }
                }
            },
            "total_visites": {
                "type": "integer",
                "description": "Nombre total de visites exportades"
            },
            "visites": {
                "type": "array",
                "description": "Llista de visites",
                "items": {
                    "type": "object",
                    "required": ["id_visita", "data", "hora", "diagnostic", "pacient", "metge"],
                    "properties": {
                        "id_visita": {
                            "type": "integer",
                            "description": "Identificador únic de la visita"
                        },
                        "data": {
                            "type": "string",
                            "format": "date",
                            "description": "Data de la visita (YYYY-MM-DD)"
                        },
                        "hora": {
                            "type": "string",
                            "description": "Hora de la visita (HH:MM:SS)"
                        },
                        "diagnostic": {
                            "type": "string",
                            "description": "Diagnòstic de la visita"
                        },
                        "pacient": {
                            "type": "object",
                            "required": ["id_pacient", "nom", "cognoms", "data_naixement", "telefon"],
                            "properties": {
                                "id_pacient": {
                                    "type": "integer",
                                    "description": "Identificador únic del pacient"
                                },
                                "nom": {
                                    "type": "string",
                                    "description": "Nom del pacient"
                                },
                                "cognoms": {
                                    "type": "string",
                                    "description": "Cognoms del pacient"
                                },
                                "data_naixement": {
                                    "type": "string",
                                    "format": "date",
                                    "description": "Data de naixement (YYYY-MM-DD)"
                                },
                                "telefon": {
                                    "type": "string",
                                    "description": "Telèfon del pacient"
                                }
                            }
                        },
                        "metge": {
                            "type": "object",
                            "required": ["nom", "cognoms", "especialitat"],
                            "properties": {
                                "nom": {
                                    "type": "string",
                                    "description": "Nom del metge"
                                },
                                "cognoms": {
                                    "type": "string",
                                    "description": "Cognoms del metge"
                                },
                                "especialitat": {
                                    "type": "string",
                                    "description": "Especialitat mèdica"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Demanem on guardar el fitxer
    ruta = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialfile="visites_schema.json"
    )

    if not ruta:
        return

    # Guardem el schema indentat
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Correcte", f"JSON Schema guardat a:\n{ruta}")