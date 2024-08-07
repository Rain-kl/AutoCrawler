# data/storage.py

import pymongo
import psycopg2
from pymongo import MongoClient
from psycopg2 import sql
from contextlib import contextmanager
from config.settings import settings
from logging import getLogger

logger = getLogger("crawler.storage")


class MongoDBStorage:
    def __init__(self):
        self.client = MongoClient(settings.mongodb_url)
        self.db = self.client.get_database()

    def save_data(self, collection_name: str, data: dict):
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        logger.info(f"Inserted document with id: {result.inserted_id}")


class PostgreSQLStorage:
    def __init__(self):
        self.connection = psycopg2.connect(settings.postgres_url)

    @contextmanager
    def get_cursor(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error in transaction, rolled back: {e}")
        finally:
            cursor.close()

    def save_data(self, table_name: str, data: dict):
        with self.get_cursor() as cursor:
            columns = data.keys()
            values = [data[column] for column in columns]
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            cursor.execute(insert_query, values)
            logger.info(f"Inserted row into table {table_name}")


# 实例化全局存储实例
mongo_storage = MongoDBStorage()
postgres_storage = PostgreSQLStorage()

# 在项目中使用存储模块
sample_data = {"title": "Example Title", "author": "Example Author", "content": "Example Content"}
mongo_storage.save_data("articles", sample_data)
postgres_storage.save_data("articles", sample_data)