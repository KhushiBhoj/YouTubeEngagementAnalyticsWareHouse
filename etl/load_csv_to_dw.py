import pandas as pd
from sqlalchemy import create_engine

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