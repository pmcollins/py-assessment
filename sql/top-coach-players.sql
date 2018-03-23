SELECT p.year, p.teamId, p.playerID, m.firstName, m.lastName, m.birthCountry
FROM top_coaches c
JOIN top_award_players p ON
  p.year = c.year
  AND
  p.teamId = c.tmID
JOIN master m ON
  m.playerId = p.playerID
ORDER BY p.year DESC
