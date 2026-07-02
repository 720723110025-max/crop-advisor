"""
MongoDB database connection and utility functions for Crop Advisory System.
Implements a safe Singleton with graceful fallback when DB is unavailable.
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class _NullCollection:
    """Stub collection returned when the database is unavailable."""

    def insert_one(self, *a, **kw):
        logger.warning("DB unavailable — insert_one ignored")
        return type('R', (), {'inserted_id': None})()

    def insert_many(self, *a, **kw):
        logger.warning("DB unavailable — insert_many ignored")
        return type('R', (), {'inserted_ids': []})()

    def find_one(self, *a, **kw):
        return None

    def find(self, *a, **kw):
        return self

    def update_one(self, *a, **kw):
        return type('R', (), {'modified_count': 0})()

    def update_many(self, *a, **kw):
        return type('R', (), {'modified_count': 0})()

    def delete_one(self, *a, **kw):
        return type('R', (), {'deleted_count': 0})()

    def delete_many(self, *a, **kw):
        return type('R', (), {'deleted_count': 0})()

    def count_documents(self, *a, **kw):
        return 0

    def create_index(self, *a, **kw):
        pass

    def sort(self, *a, **kw):
        return self

    def limit(self, *a, **kw):
        return self

    def aggregate(self, *a, **kw):
        return self

    def __iter__(self):
        return iter([])


class MongoDatabase:
    """
    MongoDB database handler for the Crop Advisory System.
    Implements Singleton pattern and never raises on init failure.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._available = False
        self.client = None
        self.db = None

        try:
            from pymongo import MongoClient
            from pymongo.errors import ConnectionFailure, OperationFailure

            mongo_uri = os.environ.get('MONGO_URI', '')
            db_name = os.environ.get('MONGO_DB_NAME', 'crop_advisory_db')

            if not mongo_uri:
                logger.warning("MONGO_URI not set — running without database")
                self._initialized = True
                return

            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB!")

            self.db = self.client[db_name]
            self._create_collections()
            self._create_indexes()
            self._available = True
            logger.info(f"Using database: {db_name}")

        except Exception as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            logger.warning("App will run without database — data will not be persisted")
        finally:
            self._initialized = True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_collections(self):
        collections = [
            'users', 'crops', 'soil_data', 'disease_reports', 'weather_data',
            'fertilizer_recommendations', 'irrigation_schedules',
            'yield_predictions', 'crop_recommendations',
        ]
        existing = self.db.list_collection_names()
        for col in collections:
            if col not in existing:
                self.db.create_collection(col)

    def _create_indexes(self):
        try:
            self.db.users.create_index('username', unique=True)
            self.db.users.create_index('email', unique=True)
            self.db.users.create_index('created_at')
            self.db.soil_data.create_index('user_id')
            self.db.disease_reports.create_index([('user_id', 1), ('created_at', -1)])
            self.db.crop_recommendations.create_index([('user_id', 1), ('created_at', -1)])
            self.db.fertilizer_recommendations.create_index([('user_id', 1), ('created_at', -1)])
            self.db.irrigation_schedules.create_index([('user_id', 1), ('is_completed', 1)])
            self.db.yield_predictions.create_index([('user_id', 1), ('created_at', -1)])
        except Exception as e:
            logger.warning(f"Index creation warning: {str(e)}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_collection(self, name):
        if self._available and self.db is not None:
            return self.db[name]
        return _NullCollection()

    def insert_one(self, collection_name, data):
        result = self.get_collection(collection_name).insert_one(data)
        return str(result.inserted_id) if result.inserted_id else None

    def find_one(self, collection_name, query):
        return self.get_collection(collection_name).find_one(query)

    def find_many(self, collection_name, query, sort_field=None, sort_order=-1, limit=None):
        col = self.get_collection(collection_name)
        cursor = col.find(query)
        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def update_one(self, collection_name, query, update_data):
        result = self.get_collection(collection_name).update_one(query, {'$set': update_data})
        return result.modified_count > 0

    def delete_one(self, collection_name, query):
        result = self.get_collection(collection_name).delete_one(query)
        return result.deleted_count > 0

    def count(self, collection_name, query=None):
        return self.get_collection(collection_name).count_documents(query or {})

    def close(self):
        if self.client:
            self.client.close()


# Singleton instance — safe to import at module level
db_instance = MongoDatabase()


# Convenience helpers
def get_collection(name):
    return db_instance.get_collection(name)


def insert_one(collection_name, data):
    return db_instance.insert_one(collection_name, data)


def find_one(collection_name, query):
    return db_instance.find_one(collection_name, query)


def find_many(collection_name, query, sort_field=None, sort_order=-1, limit=None):
    return db_instance.find_many(collection_name, query, sort_field, sort_order, limit)


def update_one(collection_name, query, update_data):
    return db_instance.update_one(collection_name, query, update_data)


def delete_one(collection_name, query):
    return db_instance.delete_one(collection_name, query)


def count(collection_name, query=None):
    return db_instance.count(collection_name, query)


__all__ = [
    'MongoDatabase', 'db_instance',
    'get_collection', 'insert_one', 'find_one', 'find_many',
    'update_one', 'delete_one', 'count',
]
