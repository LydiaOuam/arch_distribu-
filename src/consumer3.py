from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
import pyspark.sql.functions as F
from pyspark.ml.feature import MinMaxScaler, VectorAssembler
from pyspark.ml.regression import GeneralizedLinearRegressionModel


spark = SparkSession.builder\
        .appName("SparkML") \
        .getOrCreate()

# Define schema for incoming messages


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
  .select("data.*") \

df = df.withColumn("model_index", col("model_index").cast("double"))
df = df.withColumn("manufacturer_index", col("manufacturer_index").cast("double"))
df = df.withColumn("transmission_index", col("transmission_index").cast("double"))
df = df.withColumn("fuelType_index", col("fuelType_index").cast("double"))
df = df.withColumn("mileage", col("mileage").cast("double"))
df = df.withColumn("tax", col("tax").cast("double"))
df = df.withColumn("mpg", col("mpg").cast("double"))
df = df.withColumn("price", col("price").cast("double"))
df = df.withColumn("year", col("year").cast("double"))

assembler = VectorAssembler(inputCols=[ "model_index","manufacturer_index",
"transmission_index","fuelType_index","tax","year","mpg","mileage"], outputCol='features',handleInvalid="skip")
output = assembler.transform(df)

# output.show()

# load the saved model
model_path = '/src/mymodel.parquet'
loaded_model = GeneralizedLinearRegressionModel.load(model_path)
spark.sparkContext.setLogLevel("WARN")

# # make predictions on the new data using the loaded model
predictions = loaded_model.transform(output)

# df  = df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")
# value = df.select("value")
# json_df = spark.read.schema(SCHEMA).json(value)
# print("hello")

query = output\
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination() 



   