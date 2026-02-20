# YouTube News Engagement Analytics Warehouse

## Overview
This project builds a **data warehouse** and **ETL pipelines** for analyzing engagement metrics from YouTube news channels. It includes:

- **Raw JSON ingestion → Clean CSV → Staging → Data Warehouse → Marts**
- Custom **marts** for top views and controversial videos
- Automated **Python ETL scripts** with clean, uniform comments

The repository demonstrates **data engineering best practices**, including staging, fact/dimension tables, and mart creation.

---

## Features

1. **ETL Pipelines**
    - Combine raw JSON files into a master CSV
    - Load CSV into staging tables
    - Transform and populate data warehouse (dim/fact tables)
    - Create marts for analytics (Top Views, Controversy Score)

2. **Custom Test Cases**
    - Validate mart calculations (total views, likes/dislikes, controversy score)
    - Ensure ordering, non-negative engagement metrics, and completeness

3. **Uniform Commenting**
    - All Python scripts and SQL files follow a consistent comment style for clarity

---

## Data

> ⚠️ **Note:** The dataset is **too large to include in this repo**.  

You can download it from the original source:  
[YouTube Dislike Dataset by Srujan](https://github.com/Suji04/YouTube-Dislike-Dataset)

Use this dataset for running the ETL scripts and performing analytics.

---

## Usage

1. Clone this repository:

```bash
git clone https://github.com/KhushiBhoj/YouTubeEngagementAnalyticsWareHouse.git
cd YouTubeEngagementAnalyticsWareHouse
```

2. Download the dataset:
Download the JSON dataset from the YouTube Dislike Dataset by Srujan and place all JSON files in:

```
data/raw_json/
```

---

## Credits

- **Dataset:** [YouTube Dislike Dataset](https://github.com/Suji04/YouTube-Dislike-Dataset)  
- **ETL Development, Debugging, Comments & Markdown Beautification:** [ChatGPT](https://chat.openai.com/)
