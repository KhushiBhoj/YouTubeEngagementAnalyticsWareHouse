import pandas as pd
from sqlalchemy import create_engine

# Create database connection
engine = create_engine("mysql+pymysql://root:$OneDirection1@localhost:3306/youtube_dw?charset=utf8mb4")

# Number of rows to process per chunk
chunksize = 5000

# Counter for loaded rows
loaded_rows = 0

# Get total number of rows in raw_videos table
total_rows = pd.read_sql("SELECT COUNT(*) as cnt FROM raw_videos", con=engine).iloc[0]['cnt']

# Columns to load from raw_videos for staging
staging_cols = ['video_id', 'published_date', 'title', 'description', 'views', 'likes', 'dislikes', 'comment_count']

# Loop through raw_videos in chunks
for offset in range(0, total_rows, chunksize):
    query = f"SELECT {','.join(staging_cols)} FROM raw_videos LIMIT {chunksize} OFFSET {offset}"
    chunk = pd.read_sql(query, con=engine)

    # Drop rows with missing video_id or published_date
    chunk = chunk.dropna(subset=['video_id', 'published_date'])

    # Clean numeric columns
    for col in ['views', 'likes', 'dislikes', 'comment_count']:
        # Convert to numeric, replace NaNs with 0, convert to int
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0).astype(int)
        # Clip negative values to 0
        chunk[col] = chunk[col].clip(lower=0)

    # Drop duplicate video_ids within this chunk
    chunk = chunk.drop_duplicates(subset=['video_id'])

    # Insert cleaned chunk into staging table
    chunk.to_sql('stg_videos', con=engine, if_exists='append', index=False, method='multi')

    # Update loaded rows counter and print progress
    loaded_rows += len(chunk)
    percent = (loaded_rows / total_rows) * 100
    print(f"Loaded {loaded_rows:,} / {total_rows:,} rows ({percent:.1f}%)")

# Final confirmation message
print("🎉 All data moved from raw_videos → stg_videos successfully!")