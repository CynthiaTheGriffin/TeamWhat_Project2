-- Instantiate database
IF EXISTS DROP TABLE player;
IF EXISTS DROP TABLE employee;
IF EXISTS DROP TABLE prize;
IF EXISTS DROP TABLE game;
IF EXISTS DROP TABLE machine;
IF EXISTS DROP TABLE purchase_history;
IF EXISTS DROP TABLE credit_history;
IF EXISTS DROP TABLE play_history
IF EXISTS DROP TABLE maintenance_history

CREATE TABLE player (
    player_id TEXT NOT NULL PRIMARY KEY,
    player_name TEXT NOT NULL,
    credit_balance DECIMAL(10,2)
);

CREATE TABLE employee (
    employee_id TEXT NOT NULL PRIMARY KEY,
    employee_name TEXT NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE prize (
    prize_id TEXT NOT NULL PRIMARY KEY,
    prize_name TEXT NOT NULL,
    cost INT
);

CREATE TABLE game (
    game_id TEXT NOT NULL PRIMARY KEY,
    game_name TEXT NOT NULL,
    cost DECIMAL(4,2)
);

s