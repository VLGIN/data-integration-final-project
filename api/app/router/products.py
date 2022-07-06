from fastapi import APIRouter
# from ..database import db
import pandas as pd

from pymongo.mongo_client import MongoClient

client = MongoClient(
    'mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/')

db = client['data-integration']

router = APIRouter(prefix='/products')


@router.get('/{product_name}')
async def search(product_name):
    print(product_name)
    phone_list = list(db['data_matching'].find(
        {product_name: {'$exists': True}}))

    for phone in phone_list:
        del phone['_id']

    # print(list(data))

    # df = pd.DataFrame(list(data))

    return {
        'data': phone_list[0][product_name]
    }
