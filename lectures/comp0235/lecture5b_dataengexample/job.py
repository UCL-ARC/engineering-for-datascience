from dataeng.analysis import analyse_spark
from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Britishlibrary").getOrCreate()
sc = spark.sparkContext

results = analyse_spark("/1850_1859", sc, "arms")
data = []
columns = ["year", "count"]
for a in results.keys():
    data.append([a, results[a]])
df = spark.createDataFrame(data, columns).coalesce(1)
df.show()
df.write.option("header","true").mode("overwrite").csv("/1850_1859_sparksubmit")
