CREATE TABLE awards_players (
  id INTEGER NOT NULL AUTO_INCREMENT,
  playerID VARCHAR(16),
  award VARCHAR(16),
  year INTEGER,
  lgID VARCHAR(4),
  note VARCHAR(16),
  pos VARCHAR(4),
  PRIMARY KEY (id)
)