from fastapi import APIRouter, Response
import requests
import os

router = APIRouter()

@router.get('/daily', status_code=200)
def get_daily(symbol, response: Response, count=200):
    headers = {
        'Accept': 'application/json'
    }

    base = f'{os.getenv("AV_API")}?apikey={os.getenv("AV_API_KEY")}'
    params = f'function=TIME_SERIES_DAILY&outputsize=full&symbol={symbol}'
    print('hola')
    r = requests.get(f'{base}&{params}', headers=headers)



    if r.status_code != 200:
        response.status_code = 401
        return {'message': 'nope'}

    return {'message': r.text}
