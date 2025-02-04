-- Task 2: Best band ever!
SELECT DISTINCT
    `origin`, SUM(`fans`) AS `nb_fans`
FROM
    metal_bands
GROUP BY
    origin
ORDER BY
    `nb_fans` DESC;
