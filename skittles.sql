-- CT60A4304 Basics of database systems - Project
-- Authors: Joona Lappalainen AND Veikka Immonen
-- Database structure


CREATE TABLE Team (
    team_ID         INT NOT NULL PRIMARY KEY,
    FK_captain_ID   INT NOT NULL,
    team_name       TEXT UNIQUE CHECK (LENGTH(team_name) <= 64),
    team_name_short TEXT UNIQUE CHECK (LENGTH(team_name_short) <= 16),
    FOREIGN KEY (FK_captain_ID) REFERENCES Player (player_ID) ON DELETE CASCADE
);


CREATE TABLE Player (
    player_ID               INT NOT NULL PRIMARY KEY,
    first_name              TEXT CHECK (LENGTH(first_name) <= 16),
    last_name               TEXT CHECK (LENGTH(last_name) <= 16),
    FK_team_ID              INT,
    FK_home_stadium_ID      INT,
    FOREIGN KEY (FK_team_ID) REFERENCES Team (team_ID) ON DELETE CASCADE,
    FOREIGN KEY (FK_home_stadium_ID) REFERENCES Stadium (stadium_ID) ON DELETE CASCADE
);


CREATE TABLE Ranking(
    rank_ID         INT NOT NULL PRIMARY KEY,
    ranking_points  INT DEFAULT 0,
    FK_team_ID      INT NOT NULL,
    FOREIGN KEY (FK_team_ID) REFERENCES Team (team_ID) ON DELETE CASCADE
);


CREATE TABLE Statistics (
    stats_ID        INT NOT NULL PRIMARY KEY,
    total_score     INT NOT NULL DEFAULT 0,
    pikes           INT NOT NULL DEFAULT 0,
    FK_player_ID    INT NOT NULL,
    FOREIGN KEY (FK_player_ID) REFERENCES Player (player_ID) ON DELETE CASCADE
);


CREATE TABLE Match (
    match_ID        INT NOT NULL PRIMARY KEY,
    FK_stadium_ID   INT NOT NULL,
    match_date      TEXT CHECK (LENGTH(match_date) <= 16),
    result_team1    INT,
    result_team2    INT,
    FK_team1_ID     INT NOT NULL,
    FK_team2_ID     INT NOT NULL,
    winner_ID       INT,
    FOREIGN KEY (FK_team1_ID) REFERENCES Team (team_ID) ON DELETE CASCADE,
    FOREIGN KEY (FK_team2_ID) REFERENCES Team (team_ID) ON DELETE CASCADE,
    FOREIGN KEY (FK_stadium_ID) REFERENCES Stadium (stadium_ID) ON DELETE CASCADE 
);


CREATE TABLE Stadium (
    stadium_ID        INT NOT NULL PRIMARY KEY,
    stadium_name      TEXT CHECK (LENGTH(stadium_name) <= 32),
    stadium_town      TEXT CHECK (LENGTH(stadium_town) <= 32),
    stadium_type      TEXT CHECK (LENGTH(stadium_type) <= 32)
);


CREATE INDEX player_team_index ON Player(FK_team_ID);
CREATE INDEX match_participants ON Match(FK_team1_ID, FK_team2_ID)
