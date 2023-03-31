from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType

WRITE_PATH = "/data"

spark = SparkSession.builder.appName('transformParquet').getOrCreate()

SCHEMA = StructType([
    StructField("ID", LongType()),
    StructField("TITLE", StringType()),
    StructField("TEXT", StringType()),
    StructField("URL", StringType()),
    StructField("IMAGE_URL", StringType()),
    StructField("PUBLISH_DATE", TimestampType()),
    StructField("AUTHOR", StringType()),
    StructField("LANGUAGE", StringType()),
    StructField("PAYS_SOURCE", StringType()),
    StructField("SENTIMENT", LongType())
])









spark.read\
    .option("multiline", "true")\
    .json(files, schema=SCHEMA)\
    .write\
    .mode('overwrite')\
    .parquet(join(WRITE_PATH, folder.split('/')[-1]))
