CREATE  PROCEDURE insertRecipient(
    IN eID INT,
    IN eType CHAR(1)
)
COMMENT 'Insert new recipient into the recipient table.'
BEGIN
    INSERT INTO Recipient()
    VALUES(eID,eType);
    SET @recID = eID;
END
-- end here

CREATE  PROCEDURE insertOrg(
    IN eID INT,
    IN eName VARCHAR(100),
    IN eFoundingCity VARCHAR(40),
    IN eFoundinngCountry VARCHAR(40),
    IN eFoundingContinent VARCHAR(15)
)
COMMENT 'Insert new organisation into the org table'

INSERT INTO Organisation()
VALUES(
    eID,
    eName,
    eFoundingCity,
    eFoundinngCountry,
    eFoundingContinent
);
-- end here

CREATE  PROCEDURE insertAff(
    IN eName VARCHAR(150),
    IN eCountry VARCHAR(40),
    IN eLocation VARCHAR(80),
    IN eState VARCHAR(50)
)
COMMENT 'Insert new affiliate into the affiliate table'
INSERT INTO Affiliate()
VALUES(
    eName,eCountry,eLocation,eState
);
-- end here

CREATE PROCEDURE insertAffTo(
    IN eID INT,
    IN eName VARCHAR(150),
    IN eCountry VARCHAR(40)
)
COMMENT 'Insert new relation between ind and affiliate'
INSERT INTO AffiliatedTo()
VALUES(
    eID,eName,eCountry
);
-- end here

CREATE PROCEDURE insertAwardTo(
    -- IN eYEAR DATE,
    -- IN eCategory VARCHAR(40),
    -- IN eID INT,
    IN eReceivedStatus VARCHAR(10),
    IN eMotivation TEXT
)
-- eYEAR,eCategory,eID, keep here if needED to be added back in later
-- BUT ITS ADDED BY THE TRIGGER WHICH LINKS THE DATA FROM THE OTHER TABLES
-- TO COMPLETE THE ENTRY
COMMENT 'Insert relation between prize and recipient'
INSERT INTO AwardedTo(ReceivedStatus,Motivation)
VALUES(eReceivedStatus,eMotivation);
-- end here


CREATE  PROCEDURE insertInd(
    IN eID INT,
    IN eName VARCHAR(50),
    IN eGender CHAR(1),
    IN ebirthDate DATE,
    IN edeathDate DATE,
    IN eBirthCity VARCHAR(40),
    IN eBirthCountry VARCHAR(40),
    IN eBirthContinent VARCHAR(15),
    IN edeathCity VARCHAR(40),
    IN edeathCountry VARCHAR(40),
    IN edeathContinent VARCHAR(15)
)
COMMENT 'Insert new individual into the individual table'
BEGIN     
    INSERT INTO Individual( ID,
                            Name,
                            Gender,
                            birthDate,
                            deathDate,
                            birthCity,
                            birthCountry,
                            birthContinent,
                            deathCity,
                            deathCountry,
                            deathContinent)
    VALUES( eID,
            eName,
            eGender,
            ebirthDate,
            edeathDate,
            eBirthCity,
            eBirthCountry,
            eBirthContinent,
            edeathCity,
            edeathCountry,
            edeathContinent
    );
    -- SET @recID = eID;
END
-- end here

CREATE  PROCEDURE insertPrize(
    eYear DATE, 
    eCategory VARCHAR(40),
    eprizeMoney DECIMAL(10, 2),
    eawardDate DATE
)
COMMENT 'Insert new prize entry into the prize table'
BEGIN
    SET @oYear = eYear;
    SET @oCategory = eCategory;

    INSERT INTO Prize
    VALUES(
        eYear,eCategory,eprizeMoney,eawardDate
    );
END
-- end here


CREATE PROCEDURE CountPhysicsAwards(OUT physicsAwardCount INT) -- return physicsAwardCount
COMMENT 'Gets the count for the total amount of times the physics award has been handed out
This will be higher then the total amount of times the award has happened due to there being 
multiple recipeints some times'
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE awardCategory VARCHAR(255); -- stores the category 
  DECLARE awardCursor CURSOR FOR SELECT category FROM AwardedTo; -- cursor to iterate the table
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  SET physicsAwardCount = 0; -- counter
  OPEN awardCursor;

  awardLoop: LOOP
    FETCH awardCursor INTO awardCategory; -- get the category string/varchar
    IF done = 1 THEN
      LEAVE awardLoop;
    END IF;

    IF awardCategory = 'physics' THEN -- check if the category is physics
      SET physicsAwardCount = physicsAwardCount + 1; -- increment if yes
    END IF;
  END LOOP;

  CLOSE awardCursor;
END
-- end here
