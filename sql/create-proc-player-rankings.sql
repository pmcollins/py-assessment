CREATE PROCEDURE player_rankings_by_awards()
BEGIN
  SELECT
    playerID,
    year,
    count(*) AS num_awards
  FROM awards_players
  GROUP BY playerID, year
  ORDER BY year DESC, num_awards DESC;
END
