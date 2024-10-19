-- Create database
DROP DATABASE IF EXISTS MoraviYum;
CREATE DATABASE IF NOT EXISTS MoraviYum;
USE MoraviYum;

-- Create tables
CREATE TABLE IF NOT EXISTS session ( 
    user_id VARCHAR(50),
    username VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS usernames (
    email VARCHAR(50),
    user_handle VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS foods (
    vendor VARCHAR(255),
    food_name VARCHAR(255),
    food_id INT(5),
    calories INT(5),
    avg_rating FLOAT
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT(5),
    user_id VARCHAR(50),
    food_id INT(5),
    rating INT(1),
    review TEXT,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);