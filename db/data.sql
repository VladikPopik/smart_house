CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'Admin123!';

CREATE DATABASE IF NOT EXISTS my_house;

GRANT ALL PRIVILEGES ON my_house.* TO 'admin'@'%';

use my_house;

CREATE TABLE `user` (    `user_login` varchar(100) NOT NULL,
    `user_name` varchar(100) DEFAULT NULL,
    `user_email` varchar(100) DEFAULT NULL,
    `tg_login` varchar(100) DEFAULT NULL,
    `is_superuser` tinyint(1) DEFAULT NULL,
    PRIMARY KEY (`user_login`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `login` (    `user_login` varchar(100) DEFAULT NULL,
    `user_password` varchar(100) DEFAULT NULL,
    KEY `user_login` (`user_login`),
    CONSTRAINT `login_ibfk_1` FOREIGN KEY (`user_login`) REFERENCES `user` (`user_login`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `budget` (    `budget_id` char(32) PRIMARY KEY,
    `ts_from` timestamp NULL DEFAULT NULL,
    `ts_to` timestamp NULL DEFAULT NULL,
    `plan_money` float DEFAULT NULL,
    `budget_type` varchar(64) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;