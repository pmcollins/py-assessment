CREATE OR REPLACE VIEW top_award_players AS
SELECT p.*, t.teamId
FROM yearly_player_award_count p
JOIN top_yearly_award_counts a ON
  a.year = p.year
  AND
  a.max_awards = p.num_awards
JOIN player_teams t ON
  t.year = p.year
  AND
  p.playerID = t.playerId
