from pymongo.mongo_client import MongoClient

client = MongoClient(
    'mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/')

db = client['data-integration2']
