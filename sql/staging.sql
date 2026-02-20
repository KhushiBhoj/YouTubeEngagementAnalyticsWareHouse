-- Drop the staging table if it already exists
DROP TABLE IF EXISTS stg_videos;

-- Create a staging table to store cleaned/processed video data
CREATE TABLE stg_videos (
    video_id VARCHAR(50),        -- YouTube video ID
    published_date DATE,         -- Video publish date as DATE type
    title TEXT,                  -- Video title
    description LONGTEXT,        -- Full video description
    views BIGINT,                -- Number of views as integer
    likes BIGINT,                -- Number of likes as integer
    dislikes BIGINT,             -- Number of dislikes as integer
    comment_count BIGINT         -- Number of comments as integer
);