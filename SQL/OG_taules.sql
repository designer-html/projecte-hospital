

-- PERSONAL (superclass)
CREATE TABLE Personal (
    id_personal INT PRIMARY KEY,
    nom VARCHAR(50),
    cognoms VARCHAR(100),
    dni VARCHAR(9),
    adreca VARCHAR(150),
    telefon VARCHAR(20)
);

-- Subtypes
CREATE TABLE Metges (
    id_personal INT PRIMARY KEY,
    especialitat VARCHAR(100),
    estudis VARCHAR(100),
    curriculum TEXT,
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Infermeria (
    id_personal INT PRIMARY KEY,
    titulacio VARCHAR(100),
    experiencia INT,
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

CREATE TABLE Varis (
    id_personal INT PRIMARY KEY,
    tipus_feina VARCHAR(100),
    FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);

-- Patients
CREATE TABLE Pacients (
    id_pacient INT PRIMARY KEY,
    nom VARCHAR(50),
    cognoms VARCHAR(100),
    data_naix DATE,
    telefon VARCHAR(20)
);

-- Location
CREATE TABLE Planta (
    num_planta INT PRIMARY KEY
);

CREATE TABLE Habitacio (
    num_habitacio INT PRIMARY KEY,
    capacitat INT,
    num_planta INT,
    FOREIGN KEY (num_planta) REFERENCES Planta(num_planta)
);


CREATE TABLE Quirofan (
    num_quirofan INT PRIMARY KEY
);

CREATE TABLE Aparells_Medics (
    id_aparell INT PRIMARY KEY,
    nom VARCHAR(100),
    tipus VARCHAR(100),
    quantitat INT,
    num_quirofan INT,
    FOREIGN KEY (num_quirofan) REFERENCES Quirofan(num_quirofan)
);


CREATE TABLE Medicament (
    id_medicament INT PRIMARY KEY,
    nom VARCHAR(100),
    descripcio TEXT
);

CREATE TABLE Visites (
    id_visita INT PRIMARY KEY,
    data DATE,
    hora TIME,
    diagnostic TEXT,
    id_pacient INT,
    id_metge INT,
    FOREIGN KEY (id_pacient) REFERENCES Pacients(id_pacient),
    FOREIGN KEY (id_metge) REFERENCES Metges(id_personal)
);

-- Prescription (N:M)
CREATE TABLE Recepta (
    id_visita INT,
    id_medicament INT,
    PRIMARY KEY (id_visita, id_medicament),
    FOREIGN KEY (id_visita) REFERENCES Visites(id_visita),
    FOREIGN KEY (id_medicament) REFERENCES Medicament(id_medicament)
);

-- Operations
CREATE TABLE Operacions (
    id_operacio INT PRIMARY KEY,
    data DATE,
    hora TIME,
    num_quirofan INT,
    FOREIGN KEY (num_quirofan) REFERENCES Quirofan(num_quirofan)
);

-- Relationships
CREATE TABLE Fa (
    id_metge INT,
    id_operacio INT,
    PRIMARY KEY (id_metge, id_operacio),
    FOREIGN KEY (id_metge) REFERENCES Metges(id_personal),
    FOREIGN KEY (id_operacio) REFERENCES Operacions(id_operacio)
);

CREATE TABLE Assistencia (
    id_infermer INT,
    id_operacio INT,
    PRIMARY KEY (id_infermer, id_operacio),
    FOREIGN KEY (id_infermer) REFERENCES Infermeria(id_personal),
    FOREIGN KEY (id_operacio) REFERENCES Operacions(id_operacio)
);

CREATE TABLE Reserva_Habitacio (
    id_pacient INT,
    num_habitacio INT,
    PRIMARY KEY (id_pacient, num_habitacio),
    FOREIGN KEY (id_pacient) REFERENCES Pacients(id_pacient),
    FOREIGN KEY (num_habitacio) REFERENCES Habitacio(num_habitacio)
);

CREATE TABLE Consulta (
    id_metge INT,
    id_pacient INT,
    PRIMARY KEY (id_metge, id_pacient),
    FOREIGN KEY (id_metge) REFERENCES Metges(id_personal),
    FOREIGN KEY (id_pacient) REFERENCES Pacients(id_pacient)
);

-- NUEVA: reserva_q (Paciente - Médico - Quirofano)
CREATE TABLE Reserva_Q (
    id_pacient INT,
    id_metge INT,
    num_quirofan INT,
    PRIMARY KEY (id_pacient, id_metge, num_quirofan),
    FOREIGN KEY (id_pacient) REFERENCES Pacients(id_pacient),
    FOREIGN KEY (id_metge) REFERENCES Metges(id_personal),
    FOREIGN KEY (num_quirofan) REFERENCES Quirofan(num_quirofan)
);

-- NUEVA: estat (Operaciones - Quirofano)
CREATE TABLE Estat (
    id_operacio INT,
    num_quirofan INT,
    PRIMARY KEY (id_operacio, num_quirofan),
    FOREIGN KEY (id_operacio) REFERENCES Operacions(id_operacio),
    FOREIGN KEY (num_quirofan) REFERENCES Quirofan(num_quirofan)
);
