
import json
import requests
import time
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct, col, lit, from_json, column

import json
import requests
import time
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct, col, lit, from_json, column
from pyspark.sql.types import StringType, FloatType, TimestampType, StructType, StructField

# Initialize Spark Session
spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()
spark.sparkContext.setLogLevel("WARN") # Reduce logging verbosity

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "aylien_news"

# Define the schema for the Aylien API data
SCHEMA = StructType([
    StructField("type", StringType()),
    StructField("id", StringType()),
    StructField("sentiment_body_p", FloatType()),
    StructField("sentiment_body_s", FloatType()),
    StructField("sentiment_title_p", FloatType()),
    StructField("sentiment_title_s", FloatType()),
    StructField("published", TimestampType())
])

# Configure Aylien API parameters
url = 'https://api.aylien.com/news/stories'
headers = {
    'X-Application-ID': 'acec876a',
    'X-Application-Key': '419ececeb9d87be8607f81a9e05bbd9f'
}
payload = {
    'aql': 'text:(Ford) AND language:en',
    'published_at.start': 'NOW-7DAYS/DAY',
    'published_at.end': 'NOW',
    'sort_by': 'published_at',
    'sort_direction': 'desc',
    'cursor': '*',
    'per_page': 100
}
# (Add your payload and headers here)

# # Initialize Kafka producer
# producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#                          value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Define a function to fetch data from Aylien API and send it to Kafka
def fetch_and_send_data():
    response = requests.get(url, headers=headers, params=payload)
    data = response.json()

    for article in data['stories']:
        row = {
            'value': 'ford',
            'id': article['id'],
            'sentiment_body_p': article['sentiment']['body']['polarity'],
            'sentiment_body_s': article['sentiment']['body']['score'],
            'sentiment_title_p': article['sentiment']['title']['polarity'],
            'sentiment_title_s': article['sentiment']['title']['score'],
            'published': article['published_at'],
            
        }
        
        df_row = spark.createDataFrame([row])
        print(row)

        # Send the data to Kafka
        df_row.write\
        .format("kafka")\
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)\
        .option("topic", KAFKA_TOPIC)\
        .save()
        print(f"Row written to topic {KAFKA_TOPIC}")


# Fetch data from Aylien API every 60 seconds
while True:
    fetch_and_send_data()
    time.sleep(2.5)


# # Read the data from Kafka topic
# df_stream = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
#     .option("subscribe", KAFKA_TOPIC) \
#     .load()

# # Deserialize the JSON data and apply the schema
# df_stream = df_stream.selectExpr("CAST(value AS STRING)") \
#     .select(from_json(column("value"), SCHEMA).alias("data")) \
#     .select("data.*")

# # Process and print the data
# df_stream.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start() \
#     .awaitTermination()
