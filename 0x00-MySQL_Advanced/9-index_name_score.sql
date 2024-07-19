-- Task 9: Optimize search and score
CREATE INDEX idx_name_first_score
USING BTREE
ON names (
    name(1),
    score
);
