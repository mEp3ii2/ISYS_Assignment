-- 1 how many physics awards have been given out 
-- CALL CountPhysicsAwards(@physicsAmount);
SELECT @physicsAmount;
 -- ends here

-- 2 the different categories of the nobel prize
SELECT * FROM prizeCats;
-- ends here

-- 3 Average age of a nobel laureate
SELECT ROUND(AVG(DATEDIFF(at.Year,i.birthDate)/365.25)) AS 'Average Age'
FROM AwardedTo at
JOIN Individual i ON at.ID = i.ID
WHERE at.Year IS NOT NULL AND i.birthDate IS NOT NULL;  -- ends here

-- 4 Amount of women who have won a nobel prize per category

SELECT p.Category, COUNT(i.ID) AS 'Amount of winners'
FROM Prize p
LEFT JOIN AwardedTo a ON p.Year = a.Year AND p.Category = a.Category
LEFT JOIN Individual i ON a.ID = i.ID
WHERE i.Gender = 'F'
GROUP BY p.Category; -- ends here

-- 5 rankings of the top ten affiliates

SELECT a.Name AS AffiliateName, a.Country AS AffiliateCountry, COUNT(at.ID) AS AffiliatedCount
FROM Affiliate a
LEFT JOIN AffiliatedTo at ON a.Name = at.Name AND a.Country = at.Country
GROUP BY a.Name, a.Country
ORDER BY AffiliatedCount DESC
LIMIT 10; -- ends here


-- 6 organisation by category
SELECT o.Name as Organisation, a.Category , DATE_FORMAT(a.Year, '%Y') AS Year
FROM AwardedTo a 
INNER JOIN Organisation o ON a.ID = o.ID
ORDER BY a.Category;
-- ends here


-- 7 Summary of nobel prizes for the last year of awards
SELECT * FROM lastNobelPrize;
 -- ends here

--  8 youngest and oldest nobel prize winner by cat
(
SELECT i.Name, a.Category, ROUND(DATEDIFF(a.Year, i.birthDate) / 365.25) AS Age
FROM AwardedTo a
LEFT JOIN Individual i ON i.ID = a.ID
WHERE DATEDIFF(a.Year, i.birthDate) / 365.25 = (
    SELECT MIN(DATEDIFF(a2.Year, i2.birthDate) / 365.25) 
    FROM AwardedTo a2
    LEFT JOIN Individual i2 ON i2.ID = a2.ID
    WHERE a2.Category = a.Category
))
UNION
(
SELECT i.Name, a.Category, ROUND(DATEDIFF(a.Year, i.birthDate) / 365.25) AS Age
FROM AwardedTo a
LEFT JOIN Individual i ON i.ID = a.ID
WHERE DATEDIFF(a.Year, i.birthDate) / 365.25 = (
    SELECT MAX(DATEDIFF(a2.Year, i2.birthDate) / 365.25) 
    FROM AwardedTo a2
    LEFT JOIN Individual i2 ON i2.ID = a2.ID
    WHERE a2.Category = a.Category
))
ORDER BY Category; -- ends here

-- 9 get a list of all current living nobel prize winners

SELECT
    r.ID AS ID,
    IF(r.type = 'I', i.Name, NULL) AS 'Name',
    IF(r.type = 'I', i.birthDate, NULL) AS BirthDate
FROM Recipient r
LEFT JOIN Individual i ON r.ID = i.ID
WHERE r.type = 'I' AND i.deathDate IS NULL; -- ends here

-- 10  top five winners count 

SELECT r.ID AS ID, IF(r.type = 'I', i.Name, o.Name) AS Name, r.type AS RecipientType, COUNT(*) AS Wins
FROM AwardedTo a
JOIN Recipient r ON a.ID = r.ID
LEFT JOIN Individual i ON r.type = 'I' AND r.ID = i.ID
LEFT JOIN Organisation o ON r.type = 'O' AND r.ID = o.ID
GROUP BY r.ID, Name, RecipientType
ORDER BY Wins DESC
LIMIT 5; -- ends here




