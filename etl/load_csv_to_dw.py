import pandas as pd
from sqlalchemy import create_engine

<<<<<<< HEAD
# Create database connection
engine = create_engine("mysql+pymysql://root:$OneDirection1@localhost:3306/youtube_dw")

# Path to CSV file containing all raw video data
csv_file = "youtube_videos_all.csv"

# Number of rows per chunk for incremental loading
chunksize = 5000

# Read CSV in chunks and append to raw_videos table
for i, chunk in enumerate(
        pd.read_csv(csv_file, chunksize=chunksize, encoding='utf-8-sig', on_bad_lines='skip'),
        start=1
    ):
    chunk.to_sql('raw_videos', con=engine, if_exists='append', index=False)  # Insert chunk into DB
    print(f"Chunk {i} loaded successfully.")  # Progress log

# Final confirmation
print("✅ All data loaded into raw_videos (no cleaning)")
=======
# === 1. Connect to your DW ===
engine = create_engine("mysql+pymysql://root:$OneDirection1@localhost:3306/youtube_dw")

# === 2. CSV path ===
csv_file = "youtube_videos_all.csv"

# === 3. Chunked load to avoid memory issues ===
chunksize = 50000  # adjust as needed
total_rows = 0

for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize), start=1):
    # Rename columns to match DW table
    chunk.rename(columns={
        "id": "video_id",
        "date": "published_date",
        "view": "views",
        "like": "likes",
        "dislike": "dislikes",
        "comment": "comment_count"
    }, inplace=True)
    
    try:
        chunk.to_sql('raw_videos', con=engine, if_exists='append', index=False)
        total_rows += len(chunk)
        print(f"Chunk {i} loaded: {len(chunk)} rows | Total rows so far: {total_rows}")
    except Exception as e:
        print(f"⚠️ Error in chunk {i}: {e}")

print(f"✅ CSV loaded to staging table raw_videos | Total rows loaded: {total_rows}")
>>>>>>> af9355ae661a7cd22b1222afff40ee8d379f2633
