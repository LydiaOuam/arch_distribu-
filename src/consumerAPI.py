import json
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "aylien_news"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Consume messages from Kafka topic
for message in consumer:
    if message is not None and message.value is not None:
        try:
            data = json.loads(message.value)
            print(data)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON format")
    else:
        print("Received empty message")

    # Do something with the received message

# Fermer le consommateur Kafka
consumer.close()




# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, col, udf
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType,FloatType,TimestampType
# import pyspark.sql.functions as F
# from pyspark.ml.feature import MinMaxScaler, VectorAssembler
# from pyspark.ml.regression import GeneralizedLinearRegressionModel


# KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
# KAFKA_TOPIC = "aylien_news"
# spark = SparkSession.builder\
#         .appName("SparkML") \
#         .getOrCreate()


# SCHEMA = StructType([
#     StructField("type", StringType()),
#     StructField("id", StringType()),
#     StructField("sentiment_body_p", FloatType()),
#     StructField("sentiment_body_s", FloatType()),
#     StructField("sentiment_title_p", FloatType()),
#     StructField("sentiment_title_s", FloatType()),
#     StructField("published", TimestampType())
# ])



# # Define Kafka consumer properties

# # Subscribe to 1 topic, with headers
# df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "kafka:9092") \
#   .option("subscribe", "trafic_cars") \
#   .option("includeHeaders", "true") \
#   .load()\
# #   .select(from_json(col("value").cast("string"), SCHEMA).alias("data")) \
# #   .select("data.*") \

# query = df\
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()
# query.awaitTermination() 

# # # Initialize Kafka consumer
# # consumer = KafkaConsumer(
# #     KAFKA_TOPIC,
# #     bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
# #     auto_offset_reset="latest",
# #     enable_auto_commit=True,
# #     value_deserializer=lambda x: json.loads(x.decode("utf-8"))
# # )

# # # Consume messages from Kafka topic
# # for message in consumer:
# #     print(f"Received message: {message.value}")
# #     # Do something with the received message

# # Fermer le consommateur Kafka
# # consumer.close()