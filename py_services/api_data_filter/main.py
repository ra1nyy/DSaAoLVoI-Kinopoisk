import asyncio
from services import ReceiveDataService, HandlerDataService

if __name__ == "__main__":
    loop = asyncio.get_event_loop()


    async def main(loop):
        print('Start main loop!')
        handler_data = HandlerDataService()
        handler_data.get_filtered_movies()

        # receive_data = ReceiveDataService(handler=handler_data)
        # await receive_data.get_from_rabbitmq()
        # print(f'Listen: {receive_data.config.QUEUE_NAME}')


    loop.run_until_complete(main(loop))
    loop.run_forever()

# #
# # from pyspark.sql import SparkSession
# #
# # # Создайте SparkSession
# # spark = SparkSession.builder.appName("SelectFields").getOrCreate()
# #
# # # Пример данных
# # data = [("John", 30, "Male"), ("Alice", 25, "Female"), ("Bob", 35, "Male")]
# # columns = ["Name", "Age", "Gender"]
# #
# # # Создайте DataFrame
# # df = spark.createDataFrame(data, columns)
# #
# # # Покажите исходный DataFrame
# # print("Исходный DataFrame:")
# # df.show()
# #
# # # Выберите только определенные поля (например, "Name" и "Age")
# # selected_fields = df.select("Name", "Age")
# #
# # # Покажите DataFrame с выбранными полями
# # print("DataFrame с выбранными полями:")
# # selected_fields.show()
# #
# # # Преобразуйте DataFrame в RDD и маппинг для создания объектов
# # selected_objects = selected_fields.rdd.map(lambda row: {"Name": row["Name"], "Age": row["Age"]})
# #
# # # Соберите результат в список (может потребоваться использовать collect() осторожно)
# # result_list = selected_objects.collect()
# #
# # # Выведите результат
# # print("Результат:")
# # for obj in result_list:
# #     print(obj)
# #
# # # Остановите SparkSession
# # spark.stop()


# from pyspark.sql import SparkSession
#
# # Создайте SparkSession
# spark = SparkSession.builder.appName("MoviesTableExample").getOrCreate()
#
# # Ваш JSON-файл или данные
# json_data = '{"movies": [{"name": "film_2"}, {"name": "film_1"}]}'
#
# # Прочитайте JSON-данные в DataFrame
# df = spark.read.json(spark.sparkContext.parallelize([json_data]))
#
# # Покажите DataFrame
# df.show(truncate=False)
# # Выберите объект 'movies' и преобразуйте его в DataFrame
# movies_df = df.select("movies").selectExpr("explode(movies) as movie")
#
# # Покажите новую таблицу 'movies'
# movies_df.show(truncate=False)
