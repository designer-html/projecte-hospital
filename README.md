# 🏥 Hospital Blanes Health Center

Sistema de gestió hospitalària desenvolupat com a projecte intermodular del Cicle Formatiu de Grau Superior d'Administració de Sistemes Informàtics en Xarxa (ASIX).

---

## 📋 Descripció

Aquest projecte informatitza la gestió interna de l'Hospital de Blanes, incloent la gestió de pacients, personal mèdic, visites, operacions quirúrgiques i reserves d'habitacions. El sistema disposa d'alta disponibilitat mitjançant replicació de base de dades i còpies de seguretat automatitzades.

---

## 🗂️ Estructura del Projecte

```
hospital-blanes/
├── README.md
├── base_de_dades/
│   ├── taules.sql              ← Creació de totes les taules
│   ├── seguretat.sql           ← Rols, permisos i data masking
│   ├── manteniment.sql         ← Funcions d'alta i baixa
│   └── triggers.sql            ← Triggers de validació
├── alta_disponibilitat/
│   ├── backup_hospital.sh      ← Script de backup diari
│   └── restore_hospital.sh     ← Script de restauració
├── programacio/
│   ├── login.py                ← Punt d'entrada de l'aplicació
│   ├── manteniment.py          ← Bloc de manteniment
│   ├── manteniment_extra.py    ← Consultes de manteniment
│   ├── consultes.py            ← Bloc de consultes i informes
│   ├── exportacio.py           ← Bloc d'exportació JSON
│   ├── dummy_data.py           ← Generació de dades de prova
│   └── requirements.txt        ← Llibreries necessàries
└── documentacio/
    └── document_final.pdf
```

---

## ⚙️ Requisits Tècnics

### Node Primari — Servidor Principal (VM1)
- Sistema Operatiu: Ubuntu 22.04 LTS
- CPU: 2 vCPU | RAM: 4 GB | Disc: 40 GB
- IP: `192.168.250.3`
- PostgreSQL 14
- OpenSSL

### Node Secundari — Servidor Rèplica (VM2)
- Sistema Operatiu: Ubuntu 22.04 LTS
- CPU: 2 vCPU | RAM: 4 GB | Disc: 40 GB
- IP: `192.168.250.4`
- PostgreSQL 14

### Ordinador Client
- Sistema Operatiu: Windows 10/11 o Linux
- Python 3.10 o superior

### Llibreries Python
```
psycopg2-binary
faker
tkinter (inclosa per defecte amb Python)
```

---

## 🚀 Instal·lació i Execució

### 1. Clona el repositori
```bash
git clone https://github.com/usuari/hospital-blanes.git
cd hospital-blanes
```

### 2. Instal·la les dependències
```bash
pip install -r programacio/requirements.txt
```

### 3. Crea la base de dades al servidor
```bash
sudo -u postgres psql -c "CREATE DATABASE hospital;"
sudo -u postgres psql -d hospital -f base_de_dades/taules.sql
sudo -u postgres psql -d hospital -f base_de_dades/seguretat.sql
sudo -u postgres psql -d hospital -f base_de_dades/manteniment.sql
sudo -u postgres psql -d hospital -f base_de_dades/triggers.sql
```

### 4. Executa l'aplicació
```bash
python3 programacio/login.py
```

---

## 🔄 Alta Disponibilitat

El sistema disposa de replicació **Actiu-Passiu** amb PostgreSQL Streaming Replication entre VM1 (primari) i VM2 (standby).

En cas de fallada del node primari, promou el secundari:
```bash
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/14/main
```

---

## 💾 Backup i Restauració

### Backup manual
```bash
sudo -u postgres /usr/local/bin/backup_hospital.sh
```

Els backups es guarden a `/backups/` i s'executen automàticament cada dia a les 2:00 AM mitjançant cron. Es mantenen les **5 últimes còpies**.

### Restauració
```bash
sudo -u postgres /usr/local/bin/restore_hospital.sh
```

---

## 🔒 Seguretat

- Connexions xifrades mitjançant **SSL**
- Certificat autosignat generat amb **OpenSSL**, renovat automàticament cada mes
- **Data masking** aplicat a dades personals de pacients i personal
- Contrasenyes emmagatzemades amb hash **SHA-256**
- Rols i permisos restrictius: `admin`, `metge`, `infermer`, `consulta`

---

## 🛠️ Funcionalitats de l'Aplicació

- **Login** amb registre d'usuaris i seguretat SHA-256
- **Manteniment:** Alta/baixa de pacients, personal, visites, operacions i reserves
- **Consultes:** Informes per planta, personal, visites per dia i ranking de metges
- **Exportació:** Exportació de visites entre dates en format **JSON** amb JSON Schema
- **Dummy Data:** Generació i eliminació de dades de prova (50.000 pacients, 100.000 visites)

---

## 👥 Autors

Projecte desenvolupat per:
- **[Nom Alumne 1]**
- **[Nom Alumne 2]**

Curs 2025/2026 — ASIX | Mòduls: BD · Programació · XML/JSON
