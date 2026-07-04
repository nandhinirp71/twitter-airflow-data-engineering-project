# twitter-airflow-data-engineering-project
This is End-To-End Data Engineering Project using Airflow and Python. 

In this project, data is extracted using Twitter API, python is used to transform data, and the code is deployed on Airflow/EC2 and finally the results are saved on Amazon S3

## Optional Xquik Export Source

The ETL task can also read an exported JSON, JSONL, or CSV dataset from Xquik (`https://xquik.com`) without calling the Twitter API:

```bash
export XQUIK_EXPORT_PATH=/path/to/xquik-export.json
export TWEET_OUTPUT_PATH=refined_tweets.csv
python twitter_etl.py
```

When `XQUIK_EXPORT_PATH` is not set, configure the API path with environment variables:

```bash
export TWITTER_CONSUMER_KEY=...
export TWITTER_CONSUMER_SECRET=...
export TWITTER_ACCESS_KEY=...
export TWITTER_ACCESS_SECRET=...
export TWITTER_SCREEN_NAME=@elonmusk
export TWITTER_TWEET_COUNT=200
```
