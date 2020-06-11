"""DATABASE
MongoDB database initialization
"""

# # Installed # #
from pymongo import MongoClient
from pymongo.collection import Collection

# # Package # #
from .settings import mongo_settings as settings

__all__ = ("client", "collection")

client = MongoClient(settings.uri)
collection: Collection = client[settings.database][settings.collection]
