CREATE USER IF NOT EXISTS'admin'@'%' IDENTIFIED BY 'Admin123!';

GRANT ALL PRIVILEGES ON my_house.* TO 'admin'@'%';

CREATE DATABASE IF NOT EXISTS my_house;

use my_house;

CREATE TABLE user(
    user_login VARCHAR(100) PRIMARY KEY, 
    user_name VARCHAR(100), 
    user_email VARCHAR(100),
    tg_login VARCHAR(100), 
    is_superuser BOOLEAN
)

CREATE TABLE login(
    user_login VARCHAR(100),
    user_password VARCHAR(100),
    FOREIGN KEY (user_login)
    REFERENCES user(user_login)
    ON DELETE CASCADE
);

CREATE TABLE alerts(
    uuid CHAR(64) PRIMARY KEY,
    data TIMESTAMP NOT NULL,
    status CHAR(2)
)