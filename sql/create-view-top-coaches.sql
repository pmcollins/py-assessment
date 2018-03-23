CREATE OR REPLACE VIEW top_coaches AS
SELECT
  c.coachID,
  c.year,
  c.tmID,
  wins.totalWins
FROM coaches c
JOIN top_coach_wins wins ON
  wins.year = c.year
  AND
  wins.totalWins = (c.w + c.postw)
