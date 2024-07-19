-- Task 3: ld school band
SELECT
    band_name,
    IF(split, split - formed, 2022 - formed) AS lifespan
FROM
    metal_bands
WHERE
    INSTR(style, "Glam rock")
ORDER BY
    lifespan DESC;
