-- Populate database with small example
DELETE FROM maintenance_history;
DELETE FROM play_history;
DELETE FROM purchase_history;
DELETE FROM credit_history;
DELETE FROM prize;
DELETE FROM machine;
DELETE FROM player;
DELETE FROM employee;
DELETE FROM game;


-- game (id, name, cost)
INSERT INTO game VALUES ('27489', 'Immortal Combat', '0.50');
INSERT INTO game VALUES ('49014', 'Road Puncher', '0.50');
INSERT INTO game VALUES ('58393', 'N33D 4 5P33D', '2.00');
INSERT INTO game VALUES ('49910', 'Overtale','1.00');
INSERT INTO game VALUES ('10385', 'WakaWaka', '0.25');
INSERT INTO game VALUES ('57839', 'Rocket Order', '1.50');


-- employee (id, name, position)
INSERT INTO employee VALUES ('12345', 'Jerry Katz', 'Cashier');
INSERT INTO employee VALUES ('24601', 'Jean Valjean', 'Manager');
INSERT INTO employee VALUES ('83921', 'Robert Builder', 'Maintenance');
INSERT INTO employee VALUES ('01693', 'Kathy Rowe', 'Mascot');


-- player (id, name, balance)
INSERT INTO player VALUES ('12345', 'Syeda Safdar', '0.00');
INSERT INTO player VALUES ('86753', 'Dwight Smith', '4.20');
INSERT INTO player VALUES ('28974', 'Cynthia Xiong', '13.50');
INSERT INTO player VALUES ('13289', 'Jim Deverick', '421.01');


-- machine (id, game_id, condition)
INSERT INTO machine VALUES ('45678', '27489', 'running');
INSERT INTO machine VALUES ('45679', '27489', 'running');
INSERT INTO machine VALUES ('78362', '49014', 'out of service');
INSERT INTO machine VALUES ('78363', '49014', 'running');
INSERT INTO machine VALUES ('10024', '58393', 'running');
INSERT INTO machine VALUES ('10025', '58393', 'running');
INSERT INTO machine VALUES ('10026', '58393', 'out of service');
INSERT INTO machine VALUES ('10658','49910', 'running');
INSERT INTO machine VALUES ('23320','10385', 'running');
INSERT INTO machine VALUES ('23185','57839', 'out of service');


-- prize (id, name cost)
INSERT INTO prize VALUES ('89012', 'Action Figure', '10');
INSERT INTO prize VALUES ('66554', 'Sticker Pack', '2');
INSERT INTO prize VALUES ('69696', 'Electric Drone Toy', '50');
INSERT INTO prize VALUES ('43759', 'Cotton Candy', '5');
INSERT INTO prize VALUES ('34982', 'Small Plushie', '7');
INSERT INTO prize VALUES ('34983', 'Large Plushie', '15');


-- credit_history (player_id, timestamp, amount)
INSERT INTO credit_history VALUES ('13289', '2024-11-06 08:00:00', '421.26');
INSERT INTO credit_history VALUES ('13289', '2024-11-01 23:20:00', '-0.25');

INSERT INTO credit_history VALUES ('12345', '2024-12-06 10:30:30', '50.00');
INSERT INTO credit_history VALUES ('12345', '2024-12-06 13:50:01', '-0.50');
INSERT INTO credit_history VALUES ('12345', '2024-12-06 13:50:05', '-49.50');

INSERT INTO credit_history VALUES ('86753', '2024-12-05 23:00:00', '5.20');
INSERT INTO credit_history VALUES ('86753', '2024-12-05 23:56:04', '-0.50');
INSERT INTO credit_history VALUES ('86753', '2024-12-06 14:20:00', '-0.50');

INSERT INTO credit_history VALUES ('28974', '2024-12-06 13:01:01', '15.00');
INSERT INTO credit_history VALUES ('28974', '2024-12-06 14:50:01', '-1.00');
INSERT INTO credit_history VALUES ('28974', '2024-12-06 15:42:11', '-0.50');


-- purchase_history (player_id, timestamp, prize_id, quantity)
INSERT INTO purchase_history VALUES ('12345', '2024-12-06 13:00:00', '89012', '1');
INSERT INTO purchase_history VALUES ('13289', '2024-12-06 15:30:05', '69696', '1');
INSERT INTO purchase_history VALUES ('86753', '2024-12-06 20:13:01', '66554', '2');
INSERT INTO purchase_history VALUES ('86753', '2024-12-07 23:59:59', '34982', '10');
INSERT INTO purchase_history VALUES ('13289', '2024-12-08 15:42:23', '89012', '5');


-- play_history (machine_id, timestamp, player_id, score)
INSERT INTO play_history VALUES ('23320', '2024-11-01 23:30:00', '13289', '855030302');
INSERT INTO play_history VALUES ('78362', '2024-12-05 23:56:04', '86753', '0.0');
INSERT INTO play_history VALUES ('45679', '2024-12-06 14:20:01', '12345', '9999999');
INSERT INTO play_history VALUES ('45678', '2024-12-06 14:20:02', '86753', '10000000');
INSERT INTO play_history VALUES ('10658', '2024-12-06 15:10:01', '28974', '20');
INSERT INTO play_history VALUES ('78363', '2024-12-06 15:48:23', '28974', '615046');


-- maintenance_history (machine_id, employee_id, timestamp, employee_notes)
INSERT INTO maintenance_history VALUES ('45678', '83921', '2024-12-05 08:12:49', 'Fixed joystick');
INSERT INTO maintenance_history VALUES ('78362', '12345', '2024-12-05 17:24:45', 'Regular Maintenance');
INSERT INTO maintenance_history VALUES ('10658', '83921', '2024-12-06 12:12:12', 'Fixed Display Issues');
