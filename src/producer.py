from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType
import time
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import from_json, col
from pyspark.ml.feature import MinMaxScaler, VectorAssembler


spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "trafic_cars"

SCHEMA = StructType([
    StructField("model_index", StringType()),
    StructField("manufacturer_index", StringType()),
    StructField("transmission_index", StringType()),
    StructField("fuelType_index", StringType()),
    StructField("tax", StringType()),
    StructField("mpg", StringType()),
    StructField("year", StringType()),
    StructField("mileage", StringType()),
    StructField("price", StringType())
    ])






spark.sparkContext.setLogLevel("WARN") # Reduce logging verbosity

df = spark.read \
    .option("header","false")\
    .option("delimiter",',')\
    .schema(SCHEMA).format("csv").load("/../../../src/testdata3")\
    .withColumn("value", F.to_json( F.struct(F.col("*")) ) )\
    .withColumn("key", F.lit("key"))\
    .withColumn("value", F.encode(F.col("value"), "iso-8859-1").cast("binary"))\
    .withColumn("key", F.encode(F.col("key"), "iso-8859-1").cast("binary"))


# Write one row at a time to the topic

for row in df.collect():
    print(row)

    # # transform row to dataframe
    df_row = spark.createDataFrame([row.asDict()])

    print(df_row)
    # df_row = df.selectExpr("model"(struct([col(c) for c in df.columns])).alias("value"))
    time.sleep(2.5)


    # write to topic
    df_row.write\
        .format("kafka")\
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)\
        .option("topic", KAFKA_TOPIC)\
        .save()

    print(f"Row written to topic {KAFKA_TOPIC}")









