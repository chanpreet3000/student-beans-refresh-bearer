import pytz
import os

from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

from Logger import Logger


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            Logger.debug("Creating new DatabaseManager instance")
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        Logger.debug("Initializing DatabaseManager")
        load_dotenv()

        mongodb_uri = os.getenv('MONGODB_URI')
        db_name = os.getenv('MONGODB_DB_NAME')

        if not db_name or not mongodb_uri:
            raise ValueError("Database variables not found in environment variables")

        # Initialize connection
        Logger.debug(f"Attempting to connect to MongoDB database: {db_name}")
        self._client = MongoClient(mongodb_uri)
        self._db = self._client[db_name]
        self._credentials = self._db.credentials

        # Test connection
        self._client.server_info()
        Logger.debug(f"Successfully connected to MongoDB database: {db_name}")

    def close_connection(self):
        if hasattr(self, 'client'):
            self._client.close()
            Logger.debug("MongoDB connection closed successfully")

    def update_credential(self, email: str, bearer: str):
        details = {
            'email': email,
            'bearer': bearer
        }
        Logger.debug(f"Updating credentials", details)

        current_utc = datetime.now(pytz.utc).isoformat()

        update_doc = {
            '$set': {
                'bearer': bearer,
                'updated_at': current_utc
            },
            '$setOnInsert': {
                'created_at': current_utc
            }
        }

        result = self._credentials.update_one(
            {'email': email},
            update_doc,
            upsert=True
        )

        if result.upserted_id:
            Logger.info(f"Created new credential entry", details)
        else:
            Logger.info(f"Updated credential entry", details)

        return result
