-- Task 5: Email validation to sent
DELIMITER $$
CREATE TRIGGER update_state
BEFORE UPDATE
ON users FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email
    THEN
        SET NEW.valid_email = 0;
    END IF;
END$$
DELIMITER ;
