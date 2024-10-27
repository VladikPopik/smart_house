CREATE USER IF NOT EXISTS'admin'@'%' IDENTIFIED BY 'Admin123!';

GRANT ALL PRIVILEGES ON my_house.* TO 'admin'@'%';

CREATE DATABASE IF NOT EXISTS my_house;

use my_house;

CREATE TABLE  IF NOT EXISTS user(
    user_login VARCHAR(100) PRIMARY KEY, 
    user_name VARCHAR(100), 
    user_email VARCHAR(100),
    tg_login VARCHAR(100), 
    is_superuser BOOLEAN
)

CREATE TABLE IF NOT EXISTS  login(
    user_login VARCHAR(100),
    user_password VARCHAR(100),
    FOREIGN KEY (user_login)
    REFERENCES user(user_login)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  alerts(
    uuid CHAR(64) PRIMARY KEY,
    data TIMESTAMP NOT NULL,
    status CHAR(2)
)

CREATE TABLE IF NOT EXISTS  settingsd(
    device_name CHAR(8) PRIMARY KEY,
    device_type VARCHAR(100) NOT NULL,
    voltage FLOAT NOT NULL
)