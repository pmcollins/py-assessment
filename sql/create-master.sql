CREATE TABLE master (
  id INTEGER NOT NULL AUTO_INCREMENT,
  playerId VARCHAR(16),
  coachID VARCHAR(16),
  hofID VARCHAR(16),
  firstName VARCHAR(16),
  lastName VARCHAR(16),
  nameNote VARCHAR(16),
  nameGiven VARCHAR(16),
  nameNick VARCHAR(16),
  height INTEGER,
  weight INTEGER,
  shootCatch CHAR,
  legendsID VARCHAR(16),
  ihdbID INTEGER,
  hrefID VARCHAR(16),
  firstNHL INTEGER,
  lastNHL INTEGER,
  firstWHA INTEGER,
  lastWHA INTEGER,
  pos VARCHAR(4),
  birthYear INTEGER,
  birthMon INTEGER,
  birthDay INTEGER,
  birthCountry VARCHAR(16),
  birthState VARCHAR(4),
  birthCity VARCHAR(16),
  deathYear INTEGER,
  deathMon INTEGER,
  deathDay INTEGER,
  deathCountry VARCHAR(16),
  deathState VARCHAR(4),
  deathCity VARCHAR(16),
  PRIMARY KEY (id)
)