
-- Delete Procedure Here

CREATE PROCEDURE DeleteRecipient(
    IN recipientID INT
    )
COMMENT 'del recipient off id'
DELETE FROM Recipient WHERE ID = recipientID;



CREATE PROCEDURE DeleteOrganisation(
    IN orgID INT
    )
COMMENT 'del org off id'
DELETE FROM Organisation WHERE ID = orgID;


CREATE PROCEDURE DeleteIndividual(
    IN individualID INT
    )
COMMENT 'del ind off id'
DELETE FROM Individual WHERE ID = individualID;


CREATE PROCEDURE DeleteAffiliate(
    IN affiliateName VARCHAR(150), 
    IN affiliateCountry VARCHAR(40)
    )
COMMENT ' del aff off name and country'
DELETE FROM Affiliate WHERE Name = affiliateName AND Country = affiliateCountry;


CREATE PROCEDURE DeletePrize(
    IN prizeYear DATE, 
    IN prizeCategory VARCHAR(40)
    )
COMMENT ' del prize of year and category'
DELETE FROM Prize WHERE Year = prizeYear AND Category = prizeCategory;