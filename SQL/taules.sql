CREATE TABLE Personal (
    id_personal INT PRIMARY KEY,
    nom VARCHAR(50),
    cognoms VARCHAR(100),
    adreca VARCHAR(150),
    telefon VARCHAR(20),
    tipus_personal VARCHAR(20)
);

CREATE TABLE Metge (
    id_personal INT PRIMARY KEY,
    especialitat VARCHAR(100),
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Infermer (
    id_personal INT PRIMARY KEY,
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Personal_Vari (
    id_personal INT PRIMARY KEY,
    tipus_feina VARCHAR(100),
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Pacient (
    id_pacient INT PRIMARY KEY,
    nom VARCHAR(50),
    cognoms VARCHAR(100),
    cip VARCHAR(20),
    data_naixement DATE
);

CREATE TABLE Visita (
    id_visita INT PRIMARY KEY,
    data DATE,
    hora TIME,
    diagnostics TEXT,
    id_metge INT,
    id_pacient INT,
    FOREIGN KEY (id_metge) REFERENCES Metge(id_personal),
    FOREIGN KEY (id_pacient) REFERENCES Pacient(id_pacient)
);

CREATE TABLE Medicament (
    id_medicament INT PRIMARY KEY,
    nom VARCHAR(100),
    descripcio TEXT
);

CREATE TABLE Recepta (
    id_visita INT,
    id_medicament INT,
    dosi VARCHAR(50),
    PRIMARY KEY (id_visita, id_medicament),
    FOREIGN KEY (id_visita) REFERENCES Visita(id_visita),
    FOREIGN KEY (id_medicament) REFERENCES Medicament(id_medicament)
);

CREATE TABLE Planta (
    num_planta INT PRIMARY KEY
);

CREATE TABLE Habitacio (
    id_habitacio INT PRIMARY KEY,
    num_habitacio VARCHAR(10),
    num_planta INT,
    FOREIGN KEY (num_planta) REFERENCES Planta(num_planta)
);

CREATE TABLE Reserva_Habitacio (
    id_reserva INT PRIMARY KEY,
    data_ingres DATE,
    data_sortida DATE,
    id_pacient INT,
    id_habitacio INT,
    FOREIGN KEY (id_pacient) REFERENCES Pacient(id_pacient),
    FOREIGN KEY (id_habitacio) REFERENCES Habitacio(id_habitacio)
);

CREATE TABLE Quirofan (
    id_quirofan INT PRIMARY KEY,
    codi VARCHAR(10),
    num_planta INT,
    FOREIGN KEY (num_planta) REFERENCES Planta(num_planta)
);

CREATE TABLE Aparell_Medic (
    id_aparell INT PRIMARY KEY,
    tipus VARCHAR(100),
    quantitat INT,
    id_quirofan INT,
    FOREIGN KEY (id_quirofan) REFERENCES Quirofan(id_quirofan)
);

CREATE TABLE Operacio (
    id_operacio INT PRIMARY KEY,
    data DATE,
    hora TIME,
    id_quirofan INT,
    id_metge INT,
    id_pacient INT,
    FOREIGN KEY (id_quirofan) REFERENCES Quirofan(id_quirofan),
    FOREIGN KEY (id_metge) REFERENCES Metge(id_personal),
    FOREIGN KEY (id_pacient) REFERENCES Pacient(id_pacient)
);

CREATE TABLE Assistencia_Infermeria (
    id_operacio INT,
    id_infermer INT,
    PRIMARY KEY (id_operacio, id_infermer),
    FOREIGN KEY (id_operacio) REFERENCES Operacio(id_operacio),
    FOREIGN KEY (id_infermer) REFERENCES Infermer(id_personal)
);