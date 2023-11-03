CREATE TRIGGER afterAffiliateInsert
AFTER INSERT ON Affiliate FOR EACH ROW
    -- Insert the name, country, and @recID into the affiliateTo table
   CALL insertAffTo(@recID,NEW.Name,NEW.Country);
-- end here

CREATE TRIGGER beforeAwardedToInsert
BEFORE INSERT ON AwardedTo FOR EACH ROW
BEGIN -- Get the year and category 
    SET NEW.Year = @oYear;
    SET NEW.Category = @oCategory;
    SET NEW.ID = @recID;
END
-- end here


-- not used since the only data is from the csv which will only have valid years but good to have any way
-- and no functionality to insert entries on this table for python has been implemented yet
CREATE TRIGGER beforePrizeYear
BEFORE INSERT ON Prize FOR EACH ROW
BEGIN 
    IF NEW.Year < '1901-01-01' THEN
        SET NEW.Year = NULL;
    END IF;
END
-- end here


-- check continent is valid for the individual
CREATE TRIGGER beforeIndvContinent
BEFORE INSERT ON Individual FOR EACH ROW
BEGIN 
    IF NEW.birthContinent NOT IN ('Europe','Oceania','North America','Asia','Africa','South America') THEN
        SET NEW.birthContinent = NULL;
    END IF;

    IF NEW.deathContinent NOT IN('Europe','Oceania','North America','Asia','Africa','South America') THEN 
        SET NEW.deathContinent = NULL;
    END IF;
END 
-- end here