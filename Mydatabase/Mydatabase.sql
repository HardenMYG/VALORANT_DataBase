CREATE DATABASE IF NOT EXISTS Valorant;




CREATE TABLE IF NOT EXISTS admins (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
    team_name VARCHAR(255) PRIMARY KEY,
    country VARCHAR(255) NOT NULL,
    world_ranking INT NOT NULL,
    coach_name VARCHAR(255) NOT NULL,
    honors TEXT,
    recent_win_rate FLOAT CHECK (recent_win_rate BETWEEN 0 AND 1)
);


CREATE TABLE IF NOT EXISTS matches (
    match_name VARCHAR(255) PRIMARY KEY,
    organizer_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);


CREATE TABLE IF NOT EXISTS players (
    team_name VARCHAR(255) NOT NULL,
    player_number INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    nationality VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    PRIMARY KEY (team_name, player_number),
    FOREIGN KEY (team_name) REFERENCES teams(team_name) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS participations (
    team_name VARCHAR(255) NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (team_name, match_name),
    FOREIGN KEY (team_name) REFERENCES teams(team_name) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    FOREIGN KEY (match_name) REFERENCES matches(match_name) ON DELETE CASCADE 
);


INSERT IGNORE INTO admins (username, password) VALUES ('G', 'G');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('EDG', '中国','3','A','A','0.66');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('BLG', '中国','25','B','B','0.43');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('TE', '中国','39','C','C','0.66');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('EG', '美国','4','D','D','0.54');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('GG', '美国','8','E','E','0.69');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('OG', '美国','10','F','F','0.60');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('LOUD', '巴西','2','G','G','0.64');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('TL', '巴西','24','H','H','0.40');
INSERT IGNORE INTO teams (team_name, country,world_ranking,coach_name,honors,recent_win_rate) VALUES ('FE', '巴西','33','I','I','0.67');

INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('EDG', '1','ZmjjKK','2005-02-22','中国','决斗');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('EDG', '2','Smoggy','2005-02-22','中国','哨位');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('EDG', '3','CHICHOO','2005-02-22','中国','控场');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('EDG', '4','nobody','2005-02-22','中国','决斗');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('EDG', '5','Jieni7','2005-02-22','中国','先锋');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('LOUD', '1','Boostio','2005-02-22','巴西','哨位');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('LOUD', '2','Demon1','2005-02-22','巴西','决斗');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('LOUD', '3','jawgemo','2005-02-22','巴西','决斗');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('LOUD', '4','Ethan','2005-02-22','巴西','先锋');
INSERT IGNORE INTO players (team_name, player_number, name, birthdate, nationality, position) VALUES ('LOUD', '5','KevinC0M','2005-02-22','巴西','控场');

DELIMITER $$
CREATE TRIGGER validate_player_insert
BEFORE INSERT ON players
FOR EACH ROW
BEGIN
    DECLARE team_count INT;
    DECLARE player_count INT;
    
    SELECT COUNT(*) INTO team_count FROM teams WHERE team_name = NEW.team_name;
    IF team_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '队伍不存在，请先创建队伍';
    END IF;
    
    SELECT COUNT(*) INTO player_count FROM players WHERE team_name = NEW.team_name AND player_number = NEW.player_number;
    IF player_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该队伍的选手号码已存在';
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE update_team_name(
    IN old_team_name VARCHAR(255), 
    IN new_team_name VARCHAR(255)
)
BEGIN
    DECLARE teamExists INT DEFAULT 0;
    SELECT COUNT(*) INTO teamExists FROM teams WHERE team_name = new_team_name;
    IF teamExists > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新队伍名已存在';
    ELSE
        SELECT COUNT(*) INTO teamExists FROM teams WHERE team_name = old_team_name;
        IF teamExists > 0 THEN
            UPDATE teams SET team_name = new_team_name WHERE team_name = old_team_name;
            UPDATE participations SET team_name = new_team_name WHERE team_name = old_team_name;
            UPDATE players SET team_name = new_team_name WHERE team_name = old_team_name;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '旧队伍名不存在';
        END IF;
    END IF;
END$$
DELIMITER ;


CREATE VIEW match_info_with_teams AS
SELECT 
    m.match_name,
    m.organizer_name,
    m.start_date,
    m.end_date,
    p.team_name AS participating_team
FROM 
    matches m
JOIN 
    participations p ON m.match_name = p.match_name;