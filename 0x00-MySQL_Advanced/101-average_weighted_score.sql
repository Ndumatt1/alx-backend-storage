-- computes and store the average weighted score for all students

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Cursor to iterate over all user_ids
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @done = TRUE;

    OPEN cur;

    -- Iterate over each user_id
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF @done THEN
            LEAVE read_loop;
        END IF;

        -- Calculate total weighted score for the user
        SELECT SUM(corrections.score * projects.weight) INTO total_score
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate total weight for the user
        SELECT SUM(projects.weight) INTO total_weight
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate average weighted score
        IF total_weight > 0 THEN
            SET avg_score = total_score / total_weight;
        END IF;

        -- Update the average_score column for the user
        UPDATE users SET average_score = avg_score WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;

