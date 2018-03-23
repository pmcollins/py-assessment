SELECT
  c.year,
  w + postw AS totalWins,
  c.coachID,
  m.firstName,
  m.lastName,
  m.birthCountry,
  c.tmId
FROM coaches c
  JOIN master m ON m.coachID = c.coachID
ORDER BY year DESC, totalWins DESC
