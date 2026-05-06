-- Administrador general del sistema
CREATE ROLE admin_hospital SUPERUSER;

-- RRHH (gestiona personal)
CREATE ROLE rrhh;

-- Médicos
CREATE ROLE metge;

-- Enfermería
CREATE ROLE infermer;

-- Personal administrativo
CREATE ROLE administratiu;

-- Lectura limitada (otros usos)
CREATE ROLE consulta;


--Permisos per taules---

GRANT SELECT, INSERT, UPDATE ON Visita TO metge;
GRANT SELECT, INSERT, UPDATE ON Operacio TO metge;
GRANT SELECT ON Pacient TO metge;
GRANT SELECT ON Medicament TO metge;
GRANT SELECT ON Recepta TO metge;


---Enfermeria-----

GRANT SELECT ON Operacio TO infermer;
GRANT SELECT, INSERT ON Assistencia_Infermeria TO infermer;


---Administratiu-----

GRANT SELECT, INSERT, UPDATE ON Pacient TO administratiu;
GRANT SELECT, INSERT, UPDATE ON Visita TO administratiu;
GRANT SELECT, INSERT ON Reserva_Habitacio TO administratiu;

----Personal ----

GRANT ALL PRIVILEGES ON Personal TO rrhh;
GRANT ALL PRIVILEGES ON Metge TO rrhh;
GRANT ALL PRIVILEGES ON Infermer TO rrhh;
GRANT ALL PRIVILEGES ON Personal_Vari TO rrhh;


---Consulta ----

GRANT SELECT ON Pacient TO consulta;
GRANT SELECT ON Visita TO consulta;
GRANT SELECT ON Operacio TO consulta;
GRANT SELECT ON Quirofan TO consulta;


------TRIGGER 1: Evitar duplicar médico en operación (control lógico) -------

CREATE OR REPLACE FUNCTION validar_medico_ocupado()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Operacio
        WHERE id_metge = NEW.id_metge
        AND data = NEW.data
        AND hora = NEW.hora
    ) THEN
        RAISE EXCEPTION 'El metge ja té una operació assignada en aquest horari';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


--- Activar trigger----

CREATE TRIGGER trg_metge_ocupat
BEFORE INSERT ON Operacio
FOR EACH ROW
EXECUTE FUNCTION validar_medico_ocupado();

----- TRIGGER 2: Validar fechas de reserva de habitación------
CREATE OR REPLACE FUNCTION validar_reserva_habitacio()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_sortida < NEW.data_ingres THEN
        RAISE EXCEPTION 'La data de sortida no pot ser anterior a la d''ingrés';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


---Activar trigger2----

CREATE TRIGGER trg_validar_reserva
BEFORE INSERT OR UPDATE ON Reserva_Habitacio
FOR EACH ROW
EXECUTE FUNCTION validar_reserva_habitacio();

------Infermeres dependen de metge o planta-----

ALTER TABLE Infermer
ADD COLUMN tipus_dependencia VARCHAR(20),
ADD COLUMN id_metge_supervisor INT NULL;

CREATE OR REPLACE FUNCTION validar_dependencia_infermer()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tipus_dependencia = 'metge' AND NEW.id_metge_supervisor IS NULL THEN
        RAISE EXCEPTION 'Un infermer dependent de metge ha de tenir supervisor';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;