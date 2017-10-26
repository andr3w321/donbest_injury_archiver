SET TIME ZONE 'UTC';

DROP TABLE IF EXISTS donbest;
CREATE TABLE donbest(
    id SERIAL PRIMARY KEY,
    league VARCHAR(40),
    date DATE,
    team_name VARCHAR(80),
    player_name VARCHAR(80),
    position VARCHAR(80),
    is_red SMALLINT,
    injury VARCHAR(80),
    status VARCHAR(180),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    removed_at TIMESTAMP WITH TIME ZONE,
    match_team_id INTEGER,
    match_player_id INTEGER,
    UNIQUE (league, date, team_name, player_name, position, is_red, injury, status)
);
