import pandas as pd
from sqlalchemy import create_engine, text

# Create database connection
engine = create_engine(
    "mysql+pymysql://root:$OneDirection1@localhost:3306/youtube_dw?charset=utf8mb4"
)

# Load staging data
print("Loading staging data...")
stg = pd.read_sql("SELECT * FROM stg_videos", engine)
print("Rows in STG:", len(stg))

# Convert published_date to date type
stg['published_date'] = pd.to_datetime(stg['published_date']).dt.date

# Create dim_date table if it doesn't exist
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key DATE PRIMARY KEY,  # Date key
            year INT,                   # Year part of the date
            month INT,                  # Month part of the date
            day INT                     # Day part of the date
        )
    """))

# Create DataFrame for dim_date
dim_date_df = pd.DataFrame()
dim_date_df['date_key'] = stg['published_date'].unique()  # Unique dates from staging
dim_date_df['year'] = pd.to_datetime(dim_date_df['date_key']).dt.year
dim_date_df['month'] = pd.to_datetime(dim_date_df['date_key']).dt.month
dim_date_df['day'] = pd.to_datetime(dim_date_df['date_key']).dt.day

# Insert new dates into dim_date table
dim_date_df.to_sql(
    'dim_date',
    engine,
    if_exists='append',
    index=False,
    chunksize=10000
)
print("dim_date loaded")

# Load dim_video mapping
dim_video = pd.read_sql("SELECT video_key, video_id FROM dim_video", engine)
video_map = dict(zip(dim_video.video_id, dim_video.video_key))  # Map video_id → video_key

# Map video_key to staging data
stg['video_key'] = stg['video_id'].map(video_map)

# Remove rows with missing video_key
stg = stg.dropna(subset=['video_key'])

# Prepare fact table DataFrame
fact_df = stg[['video_key', 'published_date', 'views', 'likes', 'dislikes', 'comment_count']].copy()
fact_df.rename(columns={'published_date': 'date_key'}, inplace=True)  # Rename for fact table

print("Rows going into fact:", len(fact_df))

# Insert fact data into fact_engagement table
fact_df.to_sql(
    'fact_engagement',
    engine,
    if_exists='append',
    index=False,
    chunksize=50000
)
print("Fact loaded successfully 🔥")