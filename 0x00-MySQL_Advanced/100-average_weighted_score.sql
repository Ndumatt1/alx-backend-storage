-- Creates a stored procedure ComputeAverageScoreForUser that computes and store the average weighted score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE total_score FLOAT DEFAULT 0;
	DECLARE total_weight FLOAT DEFAULT 0;
	DECLARE avg_score FLOAT DEFAULT 0;

	SELECT SUM(corrections.score * projects.weight) INTO total_score
	FROM corrections
	INNER JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = user_id;

	IF total_weight > 0 THEN
		SET avg_score = total_score / total_weight;
	END IF;

	UPDATE users SET average_score = avg_score WHERE id = user_id;
END //

DELIMITER ;
