-- -- Create the database if it does not exist
-- CREATE DATABASE IF NOT EXISTS flights;

-- -- Use the newly created (or existing) database

-- \c flights;

-- Create the countries table if it does not exist
CREATE TABLE IF NOT EXISTS countries (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255),
    airports INT
);

-- Create the airports table if it does not exist
CREATE TABLE IF NOT EXISTS airports (
    icao CHAR(4) PRIMARY KEY,
    iata CHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    lat DECIMAL(10, 7),
    lon DECIMAL(10, 7),
    url VARCHAR(255),
    num_x INT,
    city VARCHAR(100),
    code CHAR(3),
    FOREIGN KEY (code) REFERENCES countries(code)
);

-- Create the airlines table if it does not exist
CREATE TABLE IF NOT EXISTS airlines (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    icao CHAR(3) NOT NULL
);
