# tests/test_storage.py

from pymongo import MongoClient
from psycopg2 import connect, sql
from data.storage import MongoDBStorage, PostgreSQLStorage


# Mock settings
class MockSettings:
    mongodb_url = "mongodb://localhost:27017/test_database"
    postgres_url = "postgresql://user:password@localhost:5432/test_database"


mock_settings = MockSettings()


# Test MongoDBStorage
def test_mongodb_storage():
    mongo_storage = MongoDBStorage(mock_settings)
    sample_data = {"title": "Test Title", "content": "Test Content"}
    mongo_storage.save_data("test_collection", sample_data)

    client = MongoClient(mock_settings.mongodb_url)
    db = client.get_database()
    collection = db["test_collection"]
    stored_data = collection.find_one({"title": "Test Title"})

    assert stored_data["content"] == "Test Content"


# Test PostgreSQLStorage
def test_postgresql_storage():
    postgres_storage = PostgreSQLStorage(mock_settings)
    sample_data = {"title": "Test Title", "content": "Test Content"}

    # Create table for testing
    conn = connect(mock_settings.postgres_url)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test_table (title TEXT, content TEXT)")
    conn.commit()

    postgres_storage.save_data("test_table", sample_data)

    cursor.execute("SELECT content FROM test_table WHERE title = 'Test Title'")
    stored_data = cursor.fetchone()

    assert stored_data[0] == "Test Content"

    cursor.execute("DROP TABLE test_table")
    conn.commit()
    cursor.close()
    conn.close()