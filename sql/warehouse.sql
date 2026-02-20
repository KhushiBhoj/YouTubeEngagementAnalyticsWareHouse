<<<<<<< HEAD
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
=======
CREATE TABLE dim_video (
    video_key INT AUTO_INCREMENT PRIMARY KEY,
    video_id VARCHAR(50) UNIQUE,
    title TEXT,
    description LONGTEXT
);
INSERT INTO dim_video (video_id, title, description)
SELECT DISTINCT video_id, title, description
FROM stg_videos;

CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);
INSERT INTO dim_date
SELECT DISTINCT
    published_date,
    YEAR(published_date),
    MONTH(published_date),
    DAY(published_date)
FROM stg_videos;

CREATE TABLE fact_engagement (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    video_key INT,
    date_key DATE,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,

    FOREIGN KEY (video_key) REFERENCES dim_video(video_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
INSERT INTO fact_engagement (video_key, date_key, views, likes, dislikes, comment_count)
SELECT
    dv.video_key,
    dd.date_key,
    s.views,
    s.likes,
    s.dislikes,
    s.comment_count
FROM stg_videos s
JOIN dim_video dv ON s.video_id = dv.video_id
JOIN dim_date dd ON s.published_date = dd.date_key;
>>>>>>> af9355ae661a7cd22b1222afff40ee8d379f2633
