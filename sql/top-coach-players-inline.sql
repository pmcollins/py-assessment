SELECT p.year, p.teamId, p.playerID, m.firstName, m.lastName, m.birthCountry
FROM (
  SELECT
    c.coachID,
    c.year,
    c.tmID
  FROM coaches c
  JOIN (
    SELECT
      c.year,
      max(w + postw) AS totalWins
    FROM coaches c
    GROUP BY c.year
  ) top
  ON
    top.year = c.year
    AND
    top.totalWins = (c.w + c.postw)
) top_coaches
JOIN (
  SELECT player_rankings.*, player_teams.teamId
  FROM (
    SELECT
      playerID,
      year,
      count(*) AS num_awards
    FROM awards_players
    GROUP BY playerID, year
  ) player_rankings JOIN (
    SELECT
      year,
      max(num_awards) max_awards
    FROM (
      SELECT
        playerID,
        year,
        count(*) AS num_awards
      FROM awards_players
      GROUP BY playerID, year
    ) t
    GROUP BY year
  ) top_awards
  ON
    player_rankings.year = top_awards.year
    AND
    player_rankings.num_awards = top_awards.max_awards
  JOIN player_teams
  ON
    player_teams.year = player_rankings.year
    AND
    player_rankings.playerID = player_teams.playerId
) p
JOIN master m ON
  m.playerId = p.playerID
WHERE
  top_coaches.year = p.year
  AND
  top_coaches.tmID = p.teamId
ORDER BY p.year DESC
