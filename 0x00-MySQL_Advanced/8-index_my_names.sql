-- Task 8: Optimize simple search
CREATE INDEX idx_name_first
USING BTREE
ON names (
    name(1)
);
