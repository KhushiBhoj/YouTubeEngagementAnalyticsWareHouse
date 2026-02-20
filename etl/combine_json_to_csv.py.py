import json
import pandas as pd
from pathlib import Path

folder_path = Path("data/raw_json")
output_csv = "youtube_videos_all.csv"

# Remove output file if exists
Path(output_csv).unlink(missing_ok=True)

for i, file in enumerate(folder_path.glob("*.json"), 1):
    print(f"Processing file {i}: {file.name}")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Clean numeric columns
    numeric_cols = ["view", "like", "dislike", "comment"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    df.fillna(0, inplace=True)
    
    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Append to CSV
    if i == 1:
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(output_csv, index=False, mode='a', header=False, encoding='utf-8-sig')