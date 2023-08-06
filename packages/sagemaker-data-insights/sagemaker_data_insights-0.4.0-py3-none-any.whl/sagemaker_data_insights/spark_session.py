import pydeequ
from pyspark.sql import SparkSession


def create_spark_session():
    spark = SparkSession.builder\
        .config("spark.jars.packages", pydeequ.deequ_maven_coord)\
        .config("spark.jars.excludes", pydeequ.f2j_maven_coord)\
        .getOrCreate()

    return spark
