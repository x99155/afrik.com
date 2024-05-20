-- Create database
--CREATE DATABASE airflow;

-- Create table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    link TEXT NOT NULL,
    date TIMESTAMP NOT NULL
);
