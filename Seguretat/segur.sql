-- =========================================
-- ESQUEMA DE SEGURETAT + DATA MASKING
-- =========================================

-- BLOQUEIG GENERAL
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- ROLES
CREATE ROLE admin;
CREATE ROLE consulta;
CREATE ROLE metge;
CREATE ROLE infermer;

-- =========================
-- PERMISOS
-- =========================

-- ADMIN
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

-- METGE
GRANT SELECT, INSERT ON Visites TO metge;
GRANT SELECT ON Pacients TO metge;
GRANT SELECT ON Operacions TO metge;

-- INFERMER
GRANT SELECT ON Operacions TO infermer;
GRANT SELECT ON Assistencia TO infermer;

-- CONSULTA
GRANT SELECT ON Visites TO consulta;
GRANT SELECT ON Operacions TO consulta;

-- =========================
-- DATA MASKING PACIENTS
-- =========================

CREATE VIEW pacients_segurs AS
SELECT
    id_pacient,
    nom,
    cognoms,
    CONCAT('*** *** ', RIGHT(telefon, 3)) AS telefon
FROM Pacients;

-- =========================
-- DATA MASKING PERSONAL
-- =========================

CREATE VIEW personal_seguretat AS
SELECT
    id_personal,
    nom,
    cognoms,
    CONCAT('******', RIGHT(dni, 2)) AS dni,
    CONCAT(SUBSTRING(telefon, 1, 2), '****') AS telefon
FROM Personal;

-- =========================
-- BLOQUEIG ACCÉS ORIGINAL
-- =========================

REVOKE SELECT ON Pacients FROM consulta;
REVOKE SELECT ON Personal FROM consulta;

GRANT SELECT ON pacients_segurs TO consulta;
GRANT SELECT ON personal_seguretat TO consulta;
