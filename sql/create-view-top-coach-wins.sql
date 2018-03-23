CREATE OR REPLACE VIEW top_coach_wins AS
SELECT
  c.year,
  max(w + postw) AS totalWins
FROM coaches c
GROUP BY c.year
