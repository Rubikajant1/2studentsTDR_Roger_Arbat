from pymongo import MongoClient
from mongodb_str import string

db_client = MongoClient(string)

database = db_client["2Students_database"]

db=database['Users']