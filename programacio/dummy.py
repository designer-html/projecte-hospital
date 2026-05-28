import psycopg2
import random
from faker import Faker
from datetime import date, timedelta

# Faker en català/espanyol i rus per alfabet ciríl·lic
fake_ca = Faker('es_ES')
fake_ru = Faker('ru_RU')  # Per dades en ciríl·lic

# ------------------ CONFIGURACIÓ BD ------------------

def connectar_bd():
    """Connecta a la base de dades PostgreSQL"""
    return psycopg2.connect(
        host="192.168.250.3",
        database="hospital",
        user="postgres",
        password="123456"
    )

# ------------------ CONSTANTS ------------------

ESPECIALITATS = [
    "Cardiologia", "Traumatologia", "Pediatria", "Neurologia",
    "Oncologia", "Dermatologia", "Psiquiatria", "Ginecologia",
    "Oftalmologia", "Urologia"
]

TITULACIONS = [
    "Grau en Infermeria", "Diplomatura en Infermeria",
    "Especialitat en Cures Intensives", "Especialitat en Pediatria"
]

TIPUS_FEINA = ["Neteja", "Administració", "Zelador", "Conductor d'Ambulància"]

DIAGNOSTICS = [
    "Hipertensió arterial", "Diabetis tipus 2", "Fractura de fèmur",
    "Pneumònia", "Infecció urinària", "Lumbàlgia", "Migranya",
    "Insuficiència cardíaca", "Asma bronquial", "Gastroenteritis"
]

MEDICAMENTS = [
    ("Ibuprofèn", "Antiinflamatori no esteroide"),
    ("Paracetamol", "Analgèsic i antipirètic"),
    ("Amoxicil·lina", "Antibiòtic de la família de les penicil·lines"),
    ("Omeprazol", "Inhibidor de la bomba de protons"),
    ("Metformina", "Antidiabètic oral"),
    ("Enalapril", "Inhibidor de l'ECA per hipertensió"),
    ("Simvastatina", "Estatina per reduir el colesterol"),
    ("Salbutamol", "Broncodilatador per asma"),
    ("Lorazepam", "Benzodiazepina ansiolítica"),
    ("Morfina", "Opioide per dolor intens")
]


# ======================================================
# CREAR DUMMY DATA
# ======================================================

def crear_dummy_data():
    """Crea totes les dades de prova a la base de dades"""
    print("Iniciant creació de dummy data...")
    conn = connectar_bd()
    cur = conn.cursor()

    try:
        # ---- PLANTES (4) ----
        print("Creant plantes...")
        for i in range(1, 5):
            cur.execute("""
                INSERT INTO Planta (num_planta)
                VALUES (%s) ON CONFLICT DO NOTHING
            """, (i,))

        # ---- HABITACIONS (20 per planta = 80 total) ----
        print("Creant habitacions...")
        num_hab = 1
        for planta in range(1, 5):
            for _ in range(20):
                cur.execute("""
                    INSERT INTO Habitacio (num_habitacio, capacitat, num_planta)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                """, (num_hab, random.randint(1, 4), planta))
                num_hab += 1

        # ---- QUIROFANS (2 per planta = 8 total) ----
        print("Creant quiròfans...")
        num_q = 1
        for planta in range(1, 5):
            for _ in range(2):
                cur.execute("""
                    INSERT INTO Quirofan (num_quirofan, num_planta)
                    VALUES (%s, %s) ON CONFLICT DO NOTHING
                """, (num_q, planta))
                num_q += 1

        # ---- APARELLS MÈDICS ----
        print("Creant aparells mèdics...")
        aparells = ["Respirador", "Màquina d'oxigen", "Monitor cardíac",
                    "Bisturí elèctric", "Làmpada quirúrgica"]
        id_aparell = 1
        for q in range(1, 9):
            for aparell in aparells:
                cur.execute("""
                    INSERT INTO Aparells_Medics (id_aparell, nom, tipus, quantitat, num_quirofan)
                    VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                """, (id_aparell, aparell, aparell, random.randint(1, 5), q))
                id_aparell += 1

        # ---- MEDICAMENTS ----
        print("Creant medicaments...")
        for i, (nom, desc) in enumerate(MEDICAMENTS, 1):
            cur.execute("""
                INSERT INTO Medicament (id_medicament, nom, descripcio)
                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
            """, (i, nom, desc))

        # ---- PERSONAL + METGES (100) ----
        print("Creant 100 metges...")
        id_personal = 1
        ids_metges = []

        for i in range(100):
            # 5% de metges amb nom ciríl·lic
            if i < 5:
                nom = fake_ru.first_name()
                cognoms = fake_ru.last_name()
            else:
                nom = fake_ca.first_name()
                cognoms = fake_ca.last_name()

            cur.execute("""
                INSERT INTO Personal (id_personal, nom, cognoms, dni, adreca, telefon)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                nom,
                cognoms,
                fake_ca.nif(),
                fake_ca.address(),
                fake_ca.phone_number()
            ))

            cur.execute("""
                INSERT INTO Metges (id_personal, especialitat, estudis, curriculum)
                VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                random.choice(ESPECIALITATS),
                f"Llicenciatura en Medicina - {fake_ca.city()}",
                f"Metge/ssa amb {random.randint(1, 30)} anys d'experiència"
            ))

            ids_metges.append(id_personal)
            id_personal += 1

        # ---- INFERMERIA (200) ----
        print("Creant 200 infermers/es...")
        ids_infermers = []

        for i in range(200):
            # 5% en ciríl·lic
            if i < 10:
                nom = fake_ru.first_name()
                cognoms = fake_ru.last_name()
            else:
                nom = fake_ca.first_name()
                cognoms = fake_ca.last_name()

            cur.execute("""
                INSERT INTO Personal (id_personal, nom, cognoms, dni, adreca, telefon)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                nom,
                cognoms,
                fake_ca.nif(),
                fake_ca.address(),
                fake_ca.phone_number()
            ))

            cur.execute("""
                INSERT INTO Infermeria (id_personal, titulacio, experiencia)
                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                random.choice(TITULACIONS),
                random.randint(0, 25)
            ))

            ids_infermers.append(id_personal)
            id_personal += 1

        # ---- ASSIGNAT (Infermeria -> Metge o Planta) ----
        print("Assignant infermers a metges...")
        for id_inf in ids_infermers:
            # 70% assignats a un metge, 30% de planta
            if random.random() < 0.7:
                cur.execute("""
                    INSERT INTO Assignat (id_infermer, id_metge)
                    VALUES (%s, %s) ON CONFLICT DO NOTHING
                """, (id_inf, random.choice(ids_metges)))

        # ---- PERSONAL VARIS: NETEJA (100) ----
        print("Creant 100 persones de neteja...")
        for _ in range(100):
            cur.execute("""
                INSERT INTO Personal (id_personal, nom, cognoms, dni, adreca, telefon)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                fake_ca.first_name(),
                fake_ca.last_name(),
                fake_ca.nif(),
                fake_ca.address(),
                fake_ca.phone_number()
            ))

            cur.execute("""
                INSERT INTO Varis (id_personal, tipus_feina)
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (id_personal, "Neteja"))

            id_personal += 1

        # ---- PERSONAL VARIS: ADMINISTRACIÓ (50) ----
        print("Creant 50 persones d'administració...")
        for _ in range(50):
            cur.execute("""
                INSERT INTO Personal (id_personal, nom, cognoms, dni, adreca, telefon)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (
                id_personal,
                fake_ca.first_name(),
                fake_ca.last_name(),
                fake_ca.nif(),
                fake_ca.address(),
                fake_ca.phone_number()
            ))

            cur.execute("""
                INSERT INTO Varis (id_personal, tipus_feina)
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (id_personal, "Administració"))

            id_personal += 1

        # ---- PACIENTS (50.000) ----
        print("Creant 50.000 pacients (pot trigar uns minuts)...")
        ids_pacients = []
        id_pacient = 1

        # Inserim en blocs de 1000 per rendiment
        bloc = []
        for i in range(50000):
            # 5% en ciríl·lic
            if i < 2500:
                nom = fake_ru.first_name()
                cognoms = fake_ru.last_name()
            else:
                nom = fake_ca.first_name()
                cognoms = fake_ca.last_name()

            data_naix = fake_ca.date_of_birth(minimum_age=0, maximum_age=95)
            telefon = fake_ca.phone_number()

            bloc.append((id_pacient, nom, cognoms, data_naix, telefon))
            ids_pacients.append(id_pacient)
            id_pacient += 1

            if len(bloc) == 1000:
                cur.executemany("""
                    INSERT INTO Pacients (id_pacient, nom, cognoms, data_naix, telefon)
                    VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                """, bloc)
                bloc = []
                print(f"  {id_pacient - 1} pacients creats...")

        if bloc:
            cur.executemany("""
                INSERT INTO Pacients (id_pacient, nom, cognoms, data_naix, telefon)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, bloc)

        # ---- VISITES (100.000) ----
        cur.execute("ALTER TABLE Visites DISABLE TRIGGER trg_visites")
        print("Creant 100.000 visites (pot trigar uns minuts)...")
        id_visita = 1
        data_base = date(2023, 1, 1)
        bloc = []

        for i in range(100000):
            data_visita = data_base + timedelta(days=random.randint(0, 730))
            hora = f"{random.randint(8, 18):02d}:{random.choice(['00', '15', '30', '45'])}:00"
            diagnostic = random.choice(DIAGNOSTICS)
            id_pac = random.choice(ids_pacients)
            id_met = random.choice(ids_metges)

            bloc.append((id_visita, data_visita, hora, diagnostic, id_pac, id_met))
            id_visita += 1

            if len(bloc) == 1000:
                cur.executemany("""
                    INSERT INTO Visites (id_visita, data, hora, diagnostic, id_pacient, id_metge)
                    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                """, bloc)
                bloc = []
                print(f"  {id_visita - 1} visites creades...")

        if bloc:
            cur.executemany("""
                INSERT INTO Visites (id_visita, data, hora, diagnostic, id_pacient, id_metge)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, bloc)

        # Tornem a activar el trigger després del dummy data
        cur.execute("ALTER TABLE Visites ENABLE TRIGGER trg_visites")
        print("Trigger de visites tornat a activar.")

        # ---- RECEPTES (algunes visites amb medicaments) ----
        print("Creant receptes...")
        cur.execute("SELECT id_visita FROM Visites ORDER BY RANDOM() LIMIT 20000")
        visites_recepta = [row[0] for row in cur.fetchall()]

        for id_vis in visites_recepta:
            id_med = random.randint(1, len(MEDICAMENTS))
            cur.execute("""
                INSERT INTO Recepta (id_visita, id_medicament)
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (id_vis, id_med))

        # ---- ÍNDEXS PER RENDIMENT ----
        print("Creant índexs...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visites_data ON Visites(data);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visites_metge ON Visites(id_metge);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visites_pacient ON Visites(id_pacient);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_pacients_cognoms ON Pacients(cognoms);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_habitacio_planta ON Habitacio(num_planta);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_operacions_data ON Operacions(data);")

        conn.commit()
        print("\n✓ Dummy data creada correctament!")
        print(f"  - 4 plantes")
        print(f"  - 80 habitacions")
        print(f"  - 8 quiròfans")
        print(f"  - 100 metges")
        print(f"  - 200 infermers/es")
        print(f"  - 150 personal varis")
        print(f"  - 50.000 pacients")
        print(f"  - 100.000 visites")
        print(f"  - 6 índexs creats")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()


# ======================================================
# ELIMINAR DUMMY DATA
# ======================================================

def eliminar_dummy_data():
    """Elimina totes les dades de prova de la base de dades"""
    print("Eliminant dummy data...")
    conn = connectar_bd()
    cur = conn.cursor()

    try:
        # Ordre important: primer les taules dependents
        taules = [
            "Recepta", "Resultat", "Assistencia", "Fa",
            "Reserva_Quirofan", "Reserva_Habitacio",
            "Visites", "Operacions", "Assignat",
            "Metges", "Infermeria", "Varis",
            "Pacients", "Personal",
            "Aparells_Medics", "Quirofan",
            "Habitacio", "Planta", "Medicament"
        ]

        for taula in taules:
            cur.execute(f"DELETE FROM {taula}")
            print(f"  {taula} eliminada")

        conn.commit()
        print("\n✓ Totes les dades dummy eliminades correctament!")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()


# ======================================================
# MENÚ PRINCIPAL
# ======================================================

if __name__ == "__main__":
    print("=" * 40)
    print("  GESTIÓ DUMMY DATA - HOSPITAL BLANES")
    print("=" * 40)
    print("1) Crear dummy data")
    print("2) Eliminar dummy data")
    opcio = input("Escull una opció (1/2): ")

    if opcio == "1":
        crear_dummy_data()
    elif opcio == "2":
        confirmar = input("Segur que vols eliminar TOTES les dades? (s/n): ")
        if confirmar.lower() == "s":
            eliminar_dummy_data()
    else:
        print("Opció no vàlida")
