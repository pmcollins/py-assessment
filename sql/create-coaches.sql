CREATE TABLE coaches (
  id INTEGER NOT NULL AUTO_INCREMENT,
  coachID VARCHAR(16),
  year INTEGER,
  tmID VARCHAR(16),
  lgID VARCHAR(16),
  stint INTEGER,
  notes VARCHAR(16),
  g INTEGER,
  w INTEGER,
  l INTEGER,
  t INTEGER,
  postg INTEGER,
  postw INTEGER,
  postl INTEGER,
  postt INTEGER,
  PRIMARY KEY (id)
)