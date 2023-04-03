from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType
import time
from pyspark.sql import SparkSession
spark = SparkSession.builder\
        .appName("SparkML") \
        .config("spark.some.config.option", "some-value")\
        .master("spark://0622870c1427:7077") \
        .config("spark.executor.memory", "3g") \
        .getOrCreate()


# df2 = spark.read.option("header","false").option("delimiter",';').csv("/../../../src/testdata")
df = spark.read.option("header","true").option("delimiter",';').csv("/../../../src/testdata")
df = df.collect()
for i in range(len(df)):
    message = df[i]  # Code pour récupérer le prochain message à envoyer
    print(message)  # Code pour envoyer le message
    time.sleep(0.1)  # Délai de 100 millisecondes entre chaque message


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

print("hello")







# spark.read\
#     .option("multiline", "true")\
#     .json(files, schema=SCHEMA)\
#     .write\
#     .mode('overwrite')\
#     .parquet(join(WRITE_PATH, folder.split('/')[-1]))
