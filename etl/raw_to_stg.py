import pandas as pd
from sqlalchemy import create_engine

<<<<<<< HEAD
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
=======
engine = create_engine("mysql+pymysql://root:$OneDirection1@localhost:3306/youtube_dw")

csv_file = "youtube_videos_all.csv"
chunksize = 5000

# Get total rows in CSV safely
with open(csv_file, encoding='utf-8', errors='ignore') as f:
    total_rows = sum(1 for _ in f) - 1  # minus header
loaded_rows = 0

for chunk in pd.read_csv(csv_file, chunksize=chunksize, encoding='utf-8', on_bad_lines='skip'):
    # Rename columns
    chunk.rename(columns={
        "id": "video_id",
        "date": "published_date",
        "view": "views",
        "like": "likes",
        "dislike": "dislikes",
        "comment": "comment_count"
    }, inplace=True)

    # Convert types
    chunk['published_date'] = pd.to_datetime(chunk['published_date'], errors='coerce')
    for col in ['views', 'likes', 'dislikes', 'comment_count']:
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0).astype(int)

    # Insert chunk safely
    try:
        chunk.to_sql('stg_videos', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f"⚠️ Failed to insert chunk starting at row {loaded_rows + 1}: {e}")
        continue

    # Update progress
    loaded_rows += len(chunk)
    print(f"Loaded {loaded_rows} / {total_rows} rows ({loaded_rows/total_rows:.1%})")

print("🎉 All CSV loaded to stg_videos")
>>>>>>> af9355ae661a7cd22b1222afff40ee8d379f2633
