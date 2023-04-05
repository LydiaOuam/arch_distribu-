from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as F
from pyspark.ml.feature import MinMaxScaler, VectorAssembler



spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()

# Define schema for incoming messages


SCHEMA = StructType([
    StructField("value", StringType()),
    StructField("manufacturer", StringType()),
    StructField("year", LongType()),
    StructField("price", LongType()),
    StructField("transmission", StringType()),
    StructField("mileage", StringType()),
    StructField("fuelType", StringType()),
    StructField("tax", LongType()),
    StructField("mpg", LongType()),
    StructField("engineSize", LongType()),
    StructField("model_index", StringType()),
    StructField("manufacturer_index", LongType()),
    StructField("transmission_index", LongType()),
    StructField("fuelType_index", LongType()),
    StructField("features", StringType()),
    StructField("featuresNormalized", StringType())
])

spark.sparkContext.setLogLevel("WARN")


# Define Kafka consumer properties

# Subscribe to 1 topic, with headers
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "trafic_cars") \
  .option("includeHeaders", "true") \
  .load()\
  .select(from_json(col("value").cast("string"), SCHEMA).alias("data")) \
  .select("data.*")





# # load the saved model
# model_path = '../../src/mymodel.parquet'
# loaded_model = GeneralizedLinearRegressionModel.load(model_path)


# # make predictions on the new data using the loaded model
# df = loaded_model.transform(scaledData)

# df  = df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")
# value = df.select("value")
# json_df = spark.read.schema(SCHEMA).json(value)
# print("hello")

query = df\
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination() 



      

