import json
import pandas as pd
from pathlib import Path

# Path to folder containing raw JSON files
folder_path = Path("data/raw_json")

# Output CSV file for combined and cleaned data
output_csv = "youtube_videos_all.csv"

# Remove old CSV if it exists
Path(output_csv).unlink(missing_ok=True)

# Loop through all JSON files in the folder
for i, file in enumerate(folder_path.glob("*.json"), 1):
    print(f"Processing file {i}: {file.name}")

    # Load JSON data
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert JSON to DataFrame
    df = pd.DataFrame(data)

    # Clean numeric columns
    numeric_cols = ["view", "like", "dislike", "comment"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Replace NaNs with 0
    df.fillna(0, inplace=True)

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop rows with missing video ID or date
    df = df.dropna(subset=['id', 'date'])

    # Drop duplicates within this file based on video ID
    df = df.drop_duplicates(subset=['id'])

    # Rename columns to match staging table
    df.rename(columns={
        "id": "video_id",
        "date": "published_date",
        "view": "views",
        "like": "likes",
        "dislike": "dislikes",
        "comment": "comment_count"
    }, inplace=True)

    # Append DataFrame to CSV
    if i == 1:
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')  # Write header for first file
    else:
        df.to_csv(output_csv, index=False, mode='a', header=False, encoding='utf-8-sig')  # Append without header

# Final message
print("🎉 JSON → Clean CSV complete!")