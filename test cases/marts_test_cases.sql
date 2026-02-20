-- Check that sum of total_views in mart matches sum of views in fact table
SELECT 
    CASE 
        WHEN SUM(total_views) = (SELECT SUM(views) FROM fact_engagement) 
        THEN 'PASS' ELSE 'FAIL' 
    END AS total_views_check
FROM mart_top_views;

-- Check that count of videos in mart matches count of unique videos in fact + dim join
SELECT 
    CASE 
        WHEN COUNT(*) = (SELECT COUNT(DISTINCT f.video_key) 
                         FROM fact_engagement f
                         JOIN dim_video dv ON f.video_key = dv.video_key) 
        THEN 'PASS' ELSE 'FAIL' 
    END AS video_count_check
FROM mart_top_views;

-- Check that mart is correctly ordered descending by total_views
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS ordering_check
FROM (
    SELECT total_views,
           LAG(total_views) OVER (ORDER BY total_views DESC) AS prev_views
    FROM mart_top_views
) t
WHERE prev_views < total_views;

-- Check that likes and dislikes sums in mart match fact table
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1
            FROM (
                SELECT dv.title,
                       SUM(f.likes) AS likes_fact,
                       SUM(f.dislikes) AS dislikes_fact,
                       m.likes AS likes_mart,
                       m.dislikes AS dislikes_mart
                FROM fact_engagement f
                JOIN dim_video dv ON f.video_key = dv.video_key
                JOIN mart_controversy m ON dv.title = m.title
                GROUP BY dv.title, m.likes, m.dislikes
            ) t
            WHERE likes_fact != likes_mart OR dislikes_fact != dislikes_mart
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS likes_dislikes_sum_check;

-- Check that controversy_score is calculated correctly with tolerance
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1
            FROM mart_controversy
            WHERE NOT (
                (likes = 0 AND controversy_score IS NULL)
                OR (likes > 0 AND ABS(controversy_score - (dislikes * 1.0 / likes)) < 0.0001)
            )
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS controversy_score_calc_check;

-- Check divide-by-zero handling
SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM mart_controversy
            WHERE likes = 0 AND controversy_score IS NOT NULL
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS divide_by_zero_check;

-- Check that mart is correctly ordered descending by controversy_score
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS controversy_ordering_check
FROM (
    SELECT controversy_score,
           LAG(controversy_score) OVER (ORDER BY controversy_score DESC) AS prev_score
    FROM mart_controversy
) t
WHERE prev_score < controversy_score;

-- Check that all videos are included in the mart
SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM dim_video dv
            WHERE NOT EXISTS (
                SELECT 1 
                FROM mart_controversy m 
                WHERE m.title = dv.title
            )
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS missing_videos_check;

-- Check that no negative likes or dislikes exist
SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM mart_controversy
            WHERE likes < 0 OR dislikes < 0
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS negative_engagement_check;