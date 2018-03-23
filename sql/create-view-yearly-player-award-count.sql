CREATE OR REPLACE VIEW yearly_player_award_count AS
SELECT
  playerID,
  year,
  count(*) AS num_awards
FROM awards_players
GROUP BY playerID, year
