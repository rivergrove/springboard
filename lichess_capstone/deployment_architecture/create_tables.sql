--drop table if exists test;
create table games (
    game_type varchar(100)
    , game_id varchar(10) not null primary key
    , utc_date date
    , utc_time time
    , white varchar(100)
    , black varchar(100)
    , result varchar(10)
    , white_elo int
    , black_elo int
    , termination varchar(50)
    , month varchar(10)
);
create table moves (
    game_id varchar(10) not null
    , move_number int not null
    , move varchar(20)
    , eval varchar(20)
    , white int
    , month varchar(10)
    , primary key (game_id, move_number)
); 