from pymongo import MongoClient
from config import MONGO_URI, MONGO
from bson import ObjectId

db = MongoClient(MONGO_URI, tz_aware=True)[MONGO['DATABASE']]
