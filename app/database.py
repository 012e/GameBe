from pymongo import MongoClient
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=1)
def get_db():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["ataxx"]
    return db["games"]

