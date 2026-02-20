<<<<<<< HEAD
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
=======
DROP TABLE IF EXISTS stg_videos;

CREATE TABLE stg_videos (
    video_id VARCHAR(50),
    published_date DATE,
    title TEXT,
    description LONGTEXT,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT
);

>>>>>>> af9355ae661a7cd22b1222afff40ee8d379f2633
