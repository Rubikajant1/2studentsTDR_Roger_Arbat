from pymongo import MongoClient

db_client = MongoClient("mongodb+srv://2studentstdr:092students@cluster0.1ktylzw.mongodb.net/")

database = db_client["2Students_database"]

db=database['Users']