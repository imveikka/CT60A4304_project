CREATE TABLE Team (
    team_ID         INT NOT NULL PRIMARY KEY,
    FK_captain_ID   INT NOT NULL,
    team_name       CHAR(64) UNIQUE,
    team_name_short CHAR(16) UNIQUE,
    FOREIGN KEY (FK_captain_ID) REFERENCES Player (player_ID)
);


CREATE TABLE Player (
    player_ID       INT NOT NULL PRIMARY KEY,
    first_name      CHAR(32),
    last_name       CHAR(32),
    FK_team_ID      INT,
    FOREIGN KEY (FK_team_ID) REFERENCES Team (team_ID)
);


CREATE TABLE Ranking(
    rank_ID         INT NOT NULL PRIMARY KEY,
    ranking_points  INT DEFAULT 0,
    FK_team_ID      INT NOT NULL,
    FOREIGN KEY (FK_team_ID) REFERENCES Team (team_ID)
);


CREATE TABLE Statistics (
    stats_ID        INT NOT NULL PRIMARY KEY,
    mean_score      REAL,
    pikes           INT NOT NULL DEFAULT 0,
    FK_player_ID    INT NOT NULL,
    FOREIGN KEY (FK_player_ID) REFERENCES Player (player_ID)
);


CREATE TABLE Match (
    match_ID        INT NOT NULL PRIMARY KEY,
    FK_stadium_ID     INT NOT NULL,
    match_date      CHAR(16),
    result_team1    INT,
    result_team2    INT,
    FK_team1_ID     INT NOT NULL,
    FK_team2_ID     INT NOT NULL,
    winner_ID       INT,
    FOREIGN KEY (FK_team1_ID) REFERENCES Team (team_ID),
    FOREIGN KEY (FK_team2_ID) REFERENCES Team (team_ID),
    FOREIGN KEY (FK_stadium_ID) REFERENCES Stadium (stadium_ID)    
);


CREATE TABLE Stadium (
    stadium_ID        INT NOT NULL PRIMARY KEY,
    stadium_name      CHAR(32),
    stadium_town      CHAR(32),
    stadium_type      CHAR(32)
);
