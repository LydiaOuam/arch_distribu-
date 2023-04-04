from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType
import time
from pyspark.sql import SparkSession

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "trafic_cars"

SCHEMA = StructType([
    StructField("value", StringType()),
    StructField("manufacturer", StringType()),
    StructField("year", StringType()),
    StructField("price", StringType()),
    StructField("transmission", StringType()),
    StructField("mileage", StringType()),
    StructField("fuelType", StringType()),
    StructField("tax", StringType()),
    StructField("mpg", StringType()),
    StructField("model_index", StringType()),
    StructField("manufacturer_index", StringType()),
    StructField("transmission_index", StringType()),
    StructField("fuelType_index", StringType()),

])


spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()



spark.sparkContext.setLogLevel("WARN") # Reduce logging verbosity

df = spark.read.option("header","false").option("delimiter",',').schema(SCHEMA).format("csv").load("/../../../src/testdata1")

# df = df.collect()
# for i in range(len(df)):
#     message = df[i]
#     print(message)  
#     time.sleep(1)

# Write one row at a time to the topic

for row in df.collect():

    # transform row to dataframe
    df_row = spark.createDataFrame([row.asDict()])
    print(df_row)
    # df_row = df.selectExpr("model"(struct([col(c) for c in df.columns])).alias("value"))

    # write to topic
    df_row.write\
        .format("kafka")\
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)\
        .option("topic", KAFKA_TOPIC)\
        .save()

    print(f"Row written to topic {KAFKA_TOPIC}")
    time.sleep(2.5)

# df_traffic_stream = spark.read.format("parquet")\
#     .schema(SCHEMA)\
#     .load(FILE_PATH)\
#     .withColumn("value", F.to_json( F.struct(F.col("*")) ) )\
#     .withColumn("key", F.lit("key"))\
#     .withColumn("value", F.encode(F.col("value"), "iso-8859-1").cast("binary"))\
#     .withColumn("key", F.encode(F.col("key"), "iso-8859-1").cast("binary"))\
#     .limit(50000)

print("hello")







# spark.read\
#     .option("multiline", "true")\
#     .json(files, schema=SCHEMA)\
#     .write\
#     .mode('overwrite')\
#     .parquet(join(WRITE_PATH, folder.split('/')[-1]))
