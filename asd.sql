SELECT 
    Player.first_name || ' ' || Player.last_name,
    (SELECT team_name_short FROM Team WHERE Team.team_ID = Player.FK_team_ID),
    pikes
FROM Statistics
INNER JOIN Player ON Player.player_id = Statistics.FK_player_id
WHERE pikes = (SELECT MAX(pikes) FROM Statistics)
ORDER BY Player.first_name;