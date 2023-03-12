SELECT
    Team.team_name_short,
    ranking_points
FROM Ranking
INNER JOIN Team ON Team.team_ID = Ranking.FK_team_ID
ORDER BY ranking_points DESC;