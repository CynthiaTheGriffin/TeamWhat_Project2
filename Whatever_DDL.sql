-- Instantiate database
DROP TABLE IF EXISTS maintenance_history;
DROP TABLE IF EXISTS play_history;
DROP TABLE IF EXISTS purchase_history;
DROP TABLE IF EXISTS credit_history;
DROP TABLE IF EXISTS prize;
DROP TABLE IF EXISTS machine;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS game;

CREATE TABLE player (
    player_id TEXT NOT NULL CHECK(LENGTH(player_id)=5),
    player_name TEXT NOT NULL,
    PRIMARY KEY (player_id)
);

CREATE TABLE employee (
    employee_id TEXT NOT NULL CHECK(LENGTH(employee_id)=5),
    employee_name TEXT NOT NULL,
    position TEXT NOT NULL,
    PRIMARY KEY (employee_id)
);

CREATE TABLE prize (
    prize_id TEXT NOT NULL CHECK(LENGTH(prize_id)=5),
    prize_name TEXT NOT NULL,
    cost INT, -- Cost in tickets
    PRIMARY KEY (prize_id)
);

CREATE TABLE game (
    game_id TEXT NOT NULL CHECK(LENGTH(game_id)=5),
    game_name TEXT NOT NULL,
    cost DECIMAL(4,2),
    PRIMARY KEY (game_id)
);

CREATE TABLE machine (
    machine_id TEXT NOT NULL CHECK(LENGTH(machine_id)=5),
    game_id TEXT NOT NULL,
    condition TEXT NOT NULL CHECK(condition IN ('running', 'out of service')),
    PRIMARY KEY (machine_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);

CREATE TABLE purchase_history (
    player_id TEXT NOT NULL,
    time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    prize_id TEXT NOT NULL,
    quantity INT CHECK(quantity > 0),
    PRIMARY KEY (player_id, time_stamp),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (prize_id) REFERENCES prize(prize_id)
);

CREATE TABLE credit_history (
    player_id TEXT NOT NULL,
    time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2),
    PRIMARY KEY (player_id, time_stamp),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

CREATE TABLE play_history (
    machine_id TEXT NOT NULL,
    time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    player_id TEXT NOT NULL,
    score TEXT NOT NULL,
    PRIMARY KEY (machine_id, time_stamp),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (machine_id) REFERENCES machine(machine_id)
);

CREATE TABLE maintenance_history (
    machine_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    employee_notes TEXT DEFAULT NULL,
    PRIMARY KEY (machine_id, time_stamp),
    FOREIGN KEY (machine_id) REFERENCES machine(machine_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);