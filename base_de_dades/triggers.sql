-- =========================================
-- TRIGGERS
-- =========================================
 
-- 1. Evitar solapament operació metge
CREATE OR REPLACE FUNCTION validar_operacio_metge()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Fa f
        JOIN Operacions o ON f.id_operacio = o.id_operacio
        WHERE f.id_metge = NEW.id_metge
          AND o.data = (SELECT data FROM Operacions WHERE id_operacio = NEW.id_operacio)
          AND o.hora = (SELECT hora FROM Operacions WHERE id_operacio = NEW.id_operacio)
          AND f.id_operacio != NEW.id_operacio
    ) THEN
        RAISE EXCEPTION 'El metge ja te una operacio en aquest horari';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
CREATE TRIGGER trg_operacio_metge
BEFORE INSERT ON Fa
FOR EACH ROW EXECUTE FUNCTION validar_operacio_metge();
 
 
-- 2. Validar reserva habitació
CREATE OR REPLACE FUNCTION validar_reserva()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_sortida_prevista < NEW.data_ingres THEN
        RAISE EXCEPTION 'La data de sortida no pot ser anterior a la data d''ingres';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
CREATE TRIGGER trg_reserva_habitacio
BEFORE INSERT OR UPDATE ON Reserva_Habitacio
FOR EACH ROW EXECUTE FUNCTION validar_reserva();
 
 
-- 3. Validar titulació infermeria
CREATE OR REPLACE FUNCTION validar_infermeria()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.titulacio IS NULL THEN
        RAISE EXCEPTION 'L''infermer/a ha de tenir titulacio';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
CREATE TRIGGER trg_infermeria
BEFORE INSERT OR UPDATE ON Infermeria
FOR EACH ROW EXECUTE FUNCTION validar_infermeria();
 
 
-- 4. Evitar duplicat visita metge-pacient mateix horari
CREATE OR REPLACE FUNCTION validar_visita()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Visites
        WHERE id_metge = NEW.id_metge
          AND data = NEW.data
          AND hora = NEW.hora
    ) THEN
        RAISE EXCEPTION 'El metge ja te una visita en aquest horari';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
CREATE TRIGGER trg_visites
BEFORE INSERT ON Visites
FOR EACH ROW EXECUTE FUNCTION validar_visita();