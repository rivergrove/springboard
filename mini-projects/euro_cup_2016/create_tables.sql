-- create tables
use euro_cup_2016;
create table asst_referee_mast(
    ass_ref_id int
    , ass_ref_name varchar(50)
    , country_id int
);
create table coach_mast(
    coach_id int
    , coach_name varchar(50)
);
create table goal_details(
    goal_id int
    , match_no int
    , player_id int
    , team_id int
    , goal_time int
    , goal_type varchar(1)
    , play_stage varchar(1)
    , goal_schedule varchar(2)
    , goal_half int
);
create table match_captain(
    match_no int
    , team_id int
    , player_captain int
);
create table match_details(
    match_no int
    , play_stage varchar(1)
    , team_id int
    , win_lose varchar(1)
    , decided_by varchar(1)
    , goal_score int
    , penalty_score varchar(1)
    , ass_ref int
    , player_gk int
);
create table match_mast(
    match_no int
    , play_stage varchar(1)
    , play_date date
    , results varchar(4)
    , decided_by varchar(1)
    , goal_score varchar(10)
    , venue_id int
    , referee_id int
    , audence int
    , plr_of_match int
    , stop1_sec int
    , stop2_sec int
);
create table penalty_gk(
    match_no int
    , team_id int
    , player_gk int
);
create table penalty_shootout(
    kick_id int
    , match_no int
    , team_id int
    , player_id int
    , score_goal varchar(1)
    , kick_no int
);
create table player_booked(
    match_no int
    , team_id int
    , player_id int
    , booking_time int
    , sent_off varchar(1)
    , play_schedule varchar(2)
    , play_half int
);
create table player_in_out(
    match_no int
    , team_id int
    , player_id int
    , in_out varchar(1)
    , time_in_out int
    , play_schedule varchar(2)
    , play_half int
);
create table player_mast(
    player_id int
    , team_id int
    , jersey_no int
    , player_name varchar(50)
    , posi_to_play varchar(2)
    , dt_of_bir date
    , age int
    , playing_club varchar(50)
);
create table playing_position(
    position_id varchar(2)
    , position_desc varchar(15)
);
create table referee_mast(
    referee_id int
    , referee_name varchar(50)
    , country_id int
);
create table soccer_city(
    city_id int
    , city varchar(50)
    , country_id int
);
create table soccer_country(
    country_id int
    , country_abbr varchar(3)
    , country_name varchar(50)
);
create table soccer_team(
    team_id int
    , team_group varchar(1)
    , match_played int
    , won int
    , draw int
    , lost int
    , goal_for int
    , goal_agnst int
    , goal_diff int
    , points int
    , group_position int
);
create table soccer_venue(
    venue_id int
    , venue_name varchar(50)
    , city_id int
    , aud_capacity int
);
create table team_coaches(
    team_id int
    , coach_id int
);

-- load data
SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/asst_referee_mast.csv' 
INTO TABLE asst_referee_mast
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(ass_ref_id,ass_ref_name,country_id);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/coach_mast.csv' 
INTO TABLE coach_mast
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(coach_id, coach_name);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/goal_details.csv' 
INTO TABLE goal_details
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(goal_id,match_no,player_id,team_id,goal_time,goal_type,play_stage,goal_schedule,goal_half);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/match_captain.csv' 
INTO TABLE match_captain
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,team_id,player_captain);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/match_details.csv' 
INTO TABLE match_details
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,play_stage,team_id,win_lose,decided_by,goal_score,penalty_score,ass_ref,player_gk);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/match_mast.csv' 
INTO TABLE match_mast
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,play_stage,play_date,results,decided_by,goal_score,venue_id,referee_id,audence,plr_of_match,stop1_sec,stop2_sec);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/penalty_gk.csv' 
INTO TABLE penalty_gk
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,team_id,player_gk);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/penalty_shootout.csv' 
INTO TABLE penalty_shootout
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(kick_id,match_no,team_id,player_id,score_goal,kick_no);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/player_booked.csv' 
INTO TABLE player_booked
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,team_id,player_id,booking_time,sent_off,play_schedule,play_half);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/player_in_out.csv' 
INTO TABLE player_in_out
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(match_no,team_id,player_id,in_out,time_in_out,play_schedule,play_half);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/player_mast.csv' 
INTO TABLE player_mast
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(player_id,team_id,jersey_no,player_name,posi_to_play,dt_of_bir,age,playing_club);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/playing_position.csv' 
INTO TABLE playing_position
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(position_id,position_desc);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/referee_mast.csv' 
INTO TABLE referee_mast
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(referee_id,referee_name,country_id);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/soccer_city.csv' 
INTO TABLE soccer_city
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(city_id,city,country_id);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/soccer_country.csv' 
INTO TABLE soccer_country
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(country_id,country_abbr,country_name);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/soccer_team.csv' 
INTO TABLE soccer_team
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(team_id,team_group,match_played,won,draw,lost,goal_for,goal_agnst,goal_diff,points,group_position);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/soccer_venue.csv' 
INTO TABLE soccer_venue
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(venue_id,venue_name,city_id,aud_capacity);

LOAD DATA LOCAL INFILE '/Users/anthonyolund/Dropbox/Code/springboard/eurocup/team_coaches.csv' 
INTO TABLE team_coaches
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(team_id,coach_id);

