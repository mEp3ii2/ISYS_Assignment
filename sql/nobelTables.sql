-- Recipient table
CREATE TABLE IF NOT EXISTS Recipient (
    ID INT PRIMARY KEY,  -- Unique number to identify recipients
    type CHAR(1) -- What type of recipient, either I or O
);

-- Organisation table
CREATE TABLE IF NOT EXISTS Organisation (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,  -- Organisation's Name
    foundingCity VARCHAR(40),  -- City the organisation was founded in
    foundingCountry VARCHAR(56),  -- Country the organisation was founded in
    foundingContinent VARCHAR(15), -- Continent the organisation was founded in
    FOREIGN KEY (ID) REFERENCES Recipient(ID)
        ON DELETE CASCADE ON UPDATE CASCADE
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Individual table
CREATE TABLE IF NOT EXISTS Individual (
    ID INT PRIMARY KEY,  -- Unique number to identify recipients
    Name VARCHAR(50) NOT NULL,  -- Individual's name
    Gender CHAR(1),  -- Gender of the individual (Male or Female only, else is null)
    birthDate DATE, -- DOB of the individual
    deathDate DATE, -- DOD of the individual
    birthCity VARCHAR(40),  -- City of birth
    birthCountry VARCHAR(56),  -- Country of birth
    birthContinent VARCHAR(15),  -- Continent of birth
    deathCity VARCHAR(40),  -- City of death
    deathCountry VARCHAR(56),  -- Country of death
    deathContinent VARCHAR(15),  -- Continent of death
    FOREIGN KEY (ID) REFERENCES Recipient (ID)
        ON DELETE CASCADE ON UPDATE CASCADE
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Affiliate table
CREATE TABLE IF NOT EXISTS Affiliate (
    Name VARCHAR(150) NOT NULL,  -- Name of affiliate group/org
    Country VARCHAR(56) NOT NULL,  -- Country of the affiliate
    Location VARCHAR(80), -- Location of the affiliate (city or region)
    State VARCHAR (50), -- State of the affiliate
    PRIMARY KEY (Name, Country) -- Composite primary key because the same institution might be in multiple countries
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Affiliate table to match recipients with their affiliates
CREATE TABLE IF NOT EXISTS AffiliatedTo (
    ID INT,  -- Unique number to identify recipients
    Name VARCHAR(150) NOT NULL,  -- Name of affiliate group/org
    Country VARCHAR(56) NOT NULL,  -- Country of the affiliate
    PRIMARY KEY (Name,Country,ID),
    FOREIGN KEY (ID) REFERENCES Recipient(ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Name, Country) REFERENCES Affiliate(Name, Country)
        ON DELETE CASCADE ON UPDATE CASCADE
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Prize table
CREATE TABLE IF NOT EXISTS Prize (
    Year DATE NOT NULL,  -- Year of award (must be on or after 1901)
    Category VARCHAR(40) NOT NULL,  -- Category of the award (must be one of the valid Nobel prize categories)
    prizeMoney DECIMAL(10, 2),  -- Cash prize in Swedish Krona (must not be negative)
    awardDate DATE,  -- Date of award (must be a year on or after 1901)
    PRIMARY KEY (Year, Category)
);

-- AwardedTo table
CREATE TABLE IF NOT EXISTS AwardedTo (
    Year DATE NOT NULL,  -- Year of award (default value of Jan 1 will be used for day and month)
    Category VARCHAR(40) NOT NULL,  -- Category of the award (must be one of the valid Nobel prize categories)
    ID INT NOT NULL,  -- Unique identifier for the awarded entry
    ReceivedStatus VARCHAR(10) NOT NULL,  -- Status on whether or not the recipient has claimed their award (values are either "received" or "restricted")
    Motivation  TEXT,
    PRIMARY KEY (Year, Category, ID),
    FOREIGN KEY (Year, Category) REFERENCES Prize(Year, Category),
    FOREIGN KEY (ID) REFERENCES Recipient(ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);