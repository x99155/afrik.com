-- Create database
CREATE DATABASE afrikdb;

-- Create table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link TEXT NOT NULL,
    date TIMESTAMP NOT NULL
);
