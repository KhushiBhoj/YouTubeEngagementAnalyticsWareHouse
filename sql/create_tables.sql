-- Drop the existing database if it exists to start fresh
DROP DATABASE IF EXISTS youtube_dw;

-- Create a new database for the YouTube data warehouse
CREATE DATABASE youtube_dw;

-- Use the newly created database
USE youtube_dw;

-- Create a raw_videos table to store raw video metadata
CREATE TABLE raw_videos (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- Unique identifier for each row
    video_id VARCHAR(50),                        -- YouTube video ID
    published_date VARCHAR(20),                  -- Video publish date as string
    title TEXT,                                  -- Video title
    description LONGTEXT,                        -- Full video description
    views VARCHAR(50),                           -- Number of views as string (raw)
    likes VARCHAR(50),                           -- Number of likes as string (raw)
    dislikes VARCHAR(50),                        -- Number of dislikes as string (raw)
    comment_count VARCHAR(50),                   -- Number of comments as string (raw)
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the row was inserted
);