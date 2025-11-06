from pymongo import MongoClient

db_client = MongoClient("mongodbString")

database = db_client["2Students_database"]

db=database['Users']
