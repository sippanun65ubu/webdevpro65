CREATE DATABASE promanagementdb CHARACTER SET utf8;
CREATE USER 'promanagementuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON promanagementuser.* TO 'promanagementuser'@'localhost';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
SET GLOBAL time_zone = 'Asia/Bangkok';