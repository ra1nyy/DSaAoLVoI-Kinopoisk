import json
import pprint

from aio_pika import connect, connect_robust, IncomingMessage
from pyspark.sql.functions import col

from settings.config import Config
from pyspark.sql import SparkSession


class HandlerDataService:
    def __init__(self):
        self.config = Config()
        self.spark = SparkSession.builder.appName("MovieDataProcessing").getOrCreate()
        self.file_path = self.config.JSON_FILE
        self.output_path = self.config.OUTPUT_JSON_FILE

        self.spark_handler = None

    def _write_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False)

    def get_filtered_movies(self):
        self.spark_handler = self.spark.read.json(self.file_path)
        # {"movies": [{"title": "harry potter 8", "year": 2008, "country": "USA", "rating": 50, "genre": "science"}]}
        docs = self.spark_handler.select("docs")
        movies = docs.withColumn("movies", docs["docs"]).drop("docs").selectExpr("explode(movies) as movie")
        # movies.show()
        # movies.printSchema()
        movies_fields = movies.select("movie.name",
                                      col("movie.genres.name").alias("genre"),
                                      "movie.year",
                                      col("movie.rating.kp").alias("rating"),
                                      col("movie.countries.name").alias("country"))
        movies_fields.show()

        # Преобразуйте DataFrame в RDD и маппинг для создания объектов
        selected_objects = movies_fields.rdd.map(
            lambda row: {"title": row["name"],
                         "year": row["year"],
                         "country": row["country"][0],
                         "rating": row["rating"],
                         "genre": row["genre"][0]})

        # Соберите результат в список (может потребоваться использовать collect() осторожно)
        result_list = selected_objects.collect()
        for obj in result_list:
            print(obj)

        # pprint.pprint(result_list)

        # movies_fields.write.json(self.output_path)

    def handle_data(self, data):
        self._write_data(data)