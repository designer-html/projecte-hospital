-- =========================================
-- FUNCIONS DE MANTENIMENT
-- =========================================
 
CREATE OR REPLACE FUNCTION alta_pacient(
    p_id INT, p_nom VARCHAR, p_cognoms VARCHAR,
    p_data_naix DATE, p_telefon VARCHAR
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Pacients(id_pacient, nom, cognoms, data_naix, telefon)
    VALUES (p_id, p_nom, p_cognoms, p_data_naix, p_telefon);
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION baixa_pacient(p_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Pacients WHERE id_pacient = p_id;
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION alta_personal(
    p_id INT, p_nom VARCHAR, p_cognoms VARCHAR,
    p_dni VARCHAR, p_adreca VARCHAR, p_telefon VARCHAR
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Personal(id_personal, nom, cognoms, dni, adreca, telefon)
    VALUES (p_id, p_nom, p_cognoms, p_dni, p_adreca, p_telefon);
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION baixa_personal(p_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Personal WHERE id_personal = p_id;
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION alta_visita(
    p_id INT, p_data DATE, p_hora TIME,
    p_diagnostic TEXT, p_pacient INT, p_metge INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Visites(id_visita, data, hora, diagnostic, id_pacient, id_metge)
    VALUES (p_id, p_data, p_hora, p_diagnostic, p_pacient, p_metge);
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION baixa_visita(p_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Visites WHERE id_visita = p_id;
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION alta_operacio(
    p_id INT, p_data DATE, p_hora TIME, p_quirofan INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Operacions(id_operacio, data, hora, num_quirofan)
    VALUES (p_id, p_data, p_hora, p_quirofan);
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION baixa_operacio(p_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Operacions WHERE id_operacio = p_id;
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION alta_reserva(
    p_pacient INT, p_habitacio INT,
    p_ingres DATE, p_sortida DATE
) RETURNS VOID AS $$
BEGIN
    IF p_sortida < p_ingres THEN
        RAISE EXCEPTION 'Data de sortida no valida';
    END IF;
    INSERT INTO Reserva_Habitacio(id_pacient, num_habitacio, data_ingres, data_sortida_prevista)
    VALUES (p_pacient, p_habitacio, p_ingres, p_sortida);
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION baixa_reserva(p_pacient INT, p_habitacio INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Reserva_Habitacio
    WHERE id_pacient = p_pacient AND num_habitacio = p_habitacio;
END;
$$ LANGUAGE plpgsql;