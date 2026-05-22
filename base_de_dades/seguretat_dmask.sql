-- =========================================
-- SEGURETAT + DATA MASKING
-- =========================================
 
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
 
CREATE ROLE admin;
CREATE ROLE metge;
CREATE ROLE infermer;
CREATE ROLE consulta;
 
-- Admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
 
-- Metge
GRANT SELECT, INSERT ON Visites    TO metge;
GRANT SELECT ON Pacients           TO metge;
GRANT SELECT ON Operacions         TO metge;
 
-- Infermer
GRANT SELECT ON Operacions         TO infermer;
GRANT SELECT ON Assistencia        TO infermer;
 
-- Consulta (vistes mascarades)
GRANT SELECT ON Visites            TO consulta;
GRANT SELECT ON Operacions         TO consulta;
 
-- Data masking Pacients
CREATE VIEW Pacients_Segurs AS
SELECT
    id_pacient,
    nom,
    cognoms,
    CONCAT('*** *** ', RIGHT(telefon, 3)) AS telefon
FROM Pacients;
 
-- Data masking Personal
CREATE VIEW Personal_Seguretat AS
SELECT
    id_personal,
    nom,
    cognoms,
    CONCAT('******', RIGHT(dni, 2))          AS dni,
    CONCAT(SUBSTRING(telefon, 1, 2), '****') AS telefon
FROM Personal;
 
REVOKE SELECT ON Pacients  FROM consulta;
REVOKE SELECT ON Personal  FROM consulta;
 
GRANT SELECT ON Pacients_Segurs    TO consulta;
GRANT SELECT ON Personal_Seguretat TO consulta;