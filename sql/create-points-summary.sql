CREATE TABLE points_summary (
  id INTEGER NOT NULL AUTO_INCREMENT,
  playerId VARCHAR(16),
  min_pts INTEGER,
  max_pts INTEGER,
  avg_pts FLOAT,
  seasons INTEGER,
  PRIMARY KEY (id)
)