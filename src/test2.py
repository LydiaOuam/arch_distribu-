from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
import pyspark.sql.functions as F
from pyspark.ml.feature import MinMaxScaler, VectorAssembler
from pyspark.ml.regression import GeneralizedLinearRegressionModel
from pyspark.ml.feature import MinMaxScaler, VectorAssembler, StringIndexer, StandardScaler, OneHotEncoder
from pyspark.sql.functions import col
from pyspark.sql import functions as f
from pyspark.ml.regression import LinearRegression, GeneralizedLinearRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.regression import GeneralizedLinearRegressionModel

spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()

df2 = spark.read.option("header","true").option("delimiter",',').csv("/data/archive-2")
df2.select([f.count(f.when(f.isnan(c)|f.col(c).isNull(),c)).alias(c) for c in df2.columns]).show()
df2 = df2.na.drop()
df2 = df2.filter(col("model") != "model")
df2 = df2.withColumn("mileage", col("mileage").cast("double"))
df2 = df2.withColumn("tax", col("tax").cast("double"))
df2 = df2.withColumn("mpg", col("mpg").cast("double"))
df2 = df2.withColumn("engineSize", col("engineSize").cast("double"))
df2 = df2.withColumn("price", col("price").cast("double"))
df2 = df2.withColumn("year", col("year").cast("double"))

categorical_features = ["model", "manufacturer", "transmission", "fuelType"]
indexers = [StringIndexer(inputCol=cat_col, outputCol=cat_col+'_index') for cat_col in categorical_features]
models =[ index.fit(df2) for index in indexers]
for model in models:
    df2 = model.transform(df2)
myData = df2["model_index","manufacturer_index" ,"transmission_index","fuelType_index","tax","mpg","year","mileage","price"]
assembler = VectorAssembler(inputCols=[ "model_index","manufacturer_index","transmission_index","fuelType_index","tax","year","mpg","mileage"], outputCol='features',handleInvalid="skip")
output = assembler.transform(myData)
scaler = MinMaxScaler(inputCol="features", outputCol="featuresNormalized")
scalerModel = scaler.fit(output)
scaledData = scalerModel.transform(output)
train_data, test_data = scaledData.randomSplit([0.7, 0.3], seed=1234)


model_path = '/src/mymodel.parquet'
loaded_model = GeneralizedLinearRegressionModel.load(model_path)

df = loaded_model.transform(test_data)
df.show()

SCHEMA = StructType([
    StructField("model_index", StringType()),
    StructField("manufacturer_index", StringType()),
    StructField("transmission_index", StringType()),
    StructField("fuelType_index", StringType()),
    StructField("tax", StringType()),
    StructField("mpg", StringType()),
    StructField("year", StringType()),
    StructField("mileage", StringType()),
    StructField("price", StringType()),
    StructField("features", StringType()),
    StructField("featuresNormalized", StringType()),
    StructField("prediction", StringType())

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





# # make predictions on the new data using the loaded model
# # df = loaded_model.transform(df.select(col("featuresNormalized"),getItem(col("featuresNormalized"))))

# # df  = df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")
# # value = df.select("value")
# # json_df = spark.read.schema(SCHEMA).json(value)
# # print("hello")

# query = df\
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#    .trigger(processingTime='2 seconds') \
#     .start()

# query.awaitTermination() 



      

