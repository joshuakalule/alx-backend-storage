-- Task 7: Average score
-- Compute and store the average score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE user_avg_score FLOAT;
    SELECT DISTINCT
        AVG(c.score) INTO user_avg_score
    FROM
        corrections AS c
    WHERE c.user_id = user_id;

    UPDATE users
    SET average_score = user_avg_score
    WHERE id = user_id;

END $$
DELIMITER ;
