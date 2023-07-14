-- Creates an index indx_name_first_score on table names and the first letter of name and score
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), LEFT(score, 1));
