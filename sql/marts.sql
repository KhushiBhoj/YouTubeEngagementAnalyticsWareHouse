<<<<<<< HEAD
-- Drop MART 1 table if it exists
DROP TABLE IF EXISTS mart_top_views;

-- Create Top Views Mart to store total views per video
CREATE TABLE mart_top_views AS
SELECT
    dv.title,                                      -- Video title
    COALESCE(SUM(f.views), 0) AS total_views       -- Total views, default 0 if no data
FROM fact_engagement f
JOIN dim_video dv ON f.video_key = dv.video_key    -- Join to video dimension
GROUP BY dv.title;                                 -- Aggregate by video title

-- Drop MART 2 table if it exists
DROP TABLE IF EXISTS mart_controversy;

-- Create Controversy Mart to store likes, dislikes, and controversy score
CREATE TABLE mart_controversy AS
SELECT
    dv.title,                                                          -- Video title
    SUM(f.likes) AS likes,                                             -- Total likes per video
    SUM(f.dislikes) AS dislikes,                                       -- Total dislikes per video
    (SUM(f.dislikes) / NULLIF(SUM(f.likes), 0)) AS controversy_score   -- Controversy score, handles divide-by-zero
FROM fact_engagement f
JOIN dim_video dv ON f.video_key = dv.video_key                        -- Join to video dimension
WHERE f.likes >= 0 AND f.dislikes >= 0                                 -- Only consider non-negative engagements
GROUP BY dv.title;                                                     -- Aggregate by video title
=======
-- MART 1 — Top Views Mart
CREATE TABLE mart_top_views AS
SELECT
    dv.title,
    SUM(f.views) AS total_views
FROM fact_engagement f
JOIN dim_video dv ON f.video_key = dv.video_key
GROUP BY dv.title
ORDER BY total_views DESC;

-- MART 2 — Controversy Mart 
CREATE TABLE mart_controversy AS
SELECT
    dv.title,
    SUM(f.likes) AS likes,
    SUM(f.dislikes) AS dislikes,
    (SUM(f.dislikes) / (SUM(f.likes)+1)) AS controversy_score
FROM fact_engagement f
JOIN dim_video dv ON f.video_key = dv.video_key
GROUP BY dv.title
ORDER BY controversy_score DESC;
>>>>>>> af9355ae661a7cd22b1222afff40ee8d379f2633
