ALTER TABLE donbest DROP CONSTRAINT donbest_league_date_team_name_player_name_position_is_red_i_key;
ALTER TABLE donbest ADD CONSTRAINT donbest_league_date_team_name_player_name_position_is_red_i_key UNIQUE (league, date, team_name, player_name, position, is_red, injury, status, removed_at);
