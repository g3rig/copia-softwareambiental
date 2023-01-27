CREATE DATABASE IF NOT EXISTS mul_monitor;

USE mul_monitor;

CREATE TABLE mul_1 (
    id_reg_mul1 INT NOT NULL AUTO_INCREMENT,
    fecha_m1 DATE NOT NULL,
    hora_m1 time NOT NULL,
    p1tmt1 real,
    p1tmt2 real,
    p1tmt3 real,
    p1tmt4 real,
    p1tp1 real,
    p1tp2 real,
    p1tp3 real,
    p1tp4 real,
    p1tp5 real,
    p1tl1 real,
    p1ts3 real,
    p1ts1 real,
    p1ts2 real,
    p2co2_2 real,
    p1co2_1 real,
    p2co2_1 real,
    PRIMARY KEY(id_reg_mul1)
);

CREATE TABLE mul_2 (
    id_reg_mul2 INT NOT NULL AUTO_INCREMENT,
    fecha_m2 DATE NOT NULL,
    hora_m2 time NOT NULL,
    p2tmt1 real,
    p2tmt2 real,
    p2tmt3 real,
    p2tmt4 real,
    p2tmt5 real,
    p2tmt6 real,
    p2tt1 real,
    p2tt2 real,
    p2tt3 real,
    p2tt4 real,
    p2tt5 real,
    p2tt6 real,
    p2tt7 real,
    co2au real,
    tempau real,
    hrau real,
    PRIMARY KEY(id_reg_mul2)
);

SELECT * FROM mul_1;
SELECT * FROM mul_2;
