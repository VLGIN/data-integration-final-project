from cmath import log
from fastapi import APIRouter

from app.helper import cursor_list_to_list
from app.models.products import PhoneSpecs
from ..database import db

router = APIRouter(prefix='/products')


@router.get('/search')
async def search(keyword: str):
    phone_list = cursor_list_to_list(db['data_matching'].find(
        {
            'name': {
                '$regex': keyword
            }
        }
    ))

    phone_name_list = sorted(set(map(lambda phone: phone['name'], phone_list)))

    return {
        'data': {
            'items': phone_name_list,
            'totalItems': len(phone_name_list)
        }
    }


@router.get('/get-specs/{product_name}')
async def get_specs(product_name, ram: str | None = None, storage: str | None = None, color: str | None = None):

    phone_list = cursor_list_to_list(db['data_matching'].find(
        {
            'name': product_name,
            'ram': {
                '$regex': ram if ram else ""
            },
            'bộ nhớ': {
                '$regex': storage if storage else ""
            },
            'màu sắc': {
                '$regex': color if color else ""
            }
        }
    ))

    ram_list = set()
    storage_list = set()
    color_list = set()

    for phone in phone_list:
        ram_list.add(phone['ram'])
        storage_list.add(phone['bộ nhớ'])
        color_list.add(phone['màu sắc'])

    return {
        'data': {
            'rams': ram_list,
            'storages': storage_list,
            'colors': color_list,
        }
    }


@router.post('/cluster')
async def get_cluster(specs: PhoneSpecs):

    phone_list = cursor_list_to_list(db['data_matching'].find(
        {
            'name': specs.name,
            'ram': specs.ram,
            'bộ nhớ': specs.storage,
            'màu sắc': specs.color,
        }
    ))[0]['data']

    chart_data_list = []

    for phone in phone_list:
        chart_data = dict()
        chart_data['unit'] = phone['source']
        chart_data['data'] = []
        chart_data['labels'] = []

        for phones_in_source in (db['unify_schema'].find({
            'name': specs.name,
            'ram': specs.ram,
            'bộ nhớ': specs.storage,
            'color': specs.color,
            'source': phone['source']
        }).sort("date")):
            if(phones_in_source['date'] not in chart_data['labels']):
                chart_data['data'].append(phones_in_source['price'])
                chart_data['labels'].append(phones_in_source['date'])

        chart_data_list.append(chart_data)

    return {
        'data': {
            'phoneList': phone_list,
            'chartDataList': chart_data_list
        }
    }
