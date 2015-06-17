BEGIN READ ONLY;
SELECT DISTINCT tags FROM (SELECT unnest(tags) AS tags FROM cjdata_dataset) tt ORDER BY tags ASC;
END;