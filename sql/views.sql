-- category list
DROP VIEW IF EXISTS prizeCats;
CREATE VIEW prizeCats AS
    SELECT DISTINCT Category
    FROM Prize;

-- last nobel prize
DROP VIEW IF EXISTS lastNobelPrize;
CREATE VIEW lastNobelPrize AS
(SELECT
    p.Category AS 'Award Category',
    a.ID AS ID,
    i.Name
    FROM Prize p 
    JOIN AwardedTo a ON a.Year = p.Year AND a.Category = p.Category
    JOIN Recipient r ON a.ID = r.ID
    LEFT JOIN Individual i ON r.ID = i.ID
    WHERE r.type ='I' AND p.Year = (SELECT MAX(Year) FROM Prize)
)
UNION
(SELECT
    p.Category AS 'Award Category',
    a.ID AS ID,
    o.Name
    FROM Prize p 
    JOIN AwardedTo a ON a.Year = p.Year AND a.Category = p.Category
    JOIN Recipient r ON a.ID = r.ID
    LEFT JOIN Organisation o ON r.ID = o.ID
    WHERE r.type ='O' AND p.Year =(SELECT MAX(Year)FROM Prize)
);