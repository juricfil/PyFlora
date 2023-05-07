DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS plants;
DROP TABLE IF EXISTS flower_pot;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    image VARBINARY NOT NULL,
    soil_moisture INT NOT NULL,
    light FLOAT NOT NULL,
    substrate TEXT
);

CREATE TABLE flower_pot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pot_name TEXT UNIQUE NOT NULL,
    plant TEXT,
    status TEXT
);

CREATE TABlE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soil_moisture INT NOT NULL,
    acidity FLOAT NOT NULL,
    lux INT NOT NULL
);