CREATE OR REPLACE VIEW top_yearly_award_counts AS
SELECT year, max(num_awards) max_awards
FROM yearly_player_award_count
GROUP BY year
