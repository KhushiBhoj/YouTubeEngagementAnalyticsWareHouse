-- Drop tables in correct order to avoid foreign key conflicts
DROP TABLE IF EXISTS fact_engagement;
DROP TABLE IF EXISTS dim_video;
DROP TABLE IF EXISTS dim_date;

-- Create dimension table for videos
CREATE TABLE dim_video (
    video_key INT AUTO_INCREMENT PRIMARY KEY,  -- Unique surrogate key for each video
    video_id VARCHAR(50) UNIQUE,               -- YouTube video ID
    title TEXT,                                -- Video title
    description LONGTEXT                       -- Full video description
);

-- Create dimension table for dates
CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,                 -- Date of the engagement
    year INT,                                  -- Year part of the date
    month INT,                                 -- Month part of the date
    day INT                                    -- Day part of the date
);

-- Create fact table for video engagement metrics
CREATE TABLE fact_engagement (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,    -- Surrogate key for fact table
    video_key INT,                             -- Foreign key to dim_video
    date_key DATE,                             -- Foreign key to dim_date
    views BIGINT,                              -- Number of views
    likes BIGINT,                              -- Number of likes
    dislikes BIGINT,                           -- Number of dislikes
    comment_count BIGINT,                      -- Number of comments

    FOREIGN KEY (video_key) REFERENCES dim_video(video_key),  -- FK to video dimension
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)      -- FK to date dimension
);