CREATE TABLE player_teams (
  id INTEGER NOT NULL AUTO_INCREMENT,
  playerId VARCHAR(16),
  teamId VARCHAR(16),
  year INTEGER,
  PRIMARY KEY (id)
)