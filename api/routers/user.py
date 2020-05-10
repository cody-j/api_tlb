from fastapi import APIRouter, Response
import requests
import os

router = APIRouter()

@router.get('/', status_code=200)
async def get_user(screen_name, response: Response):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
    }
    r = requests.get(f'https://api.twitter.com/1.1/users/show.json?screen_name={screen_name}', headers=headers)

    if r.status_code != 200:
        response.status_code = 401
        return {'message': 'nope'}

    return {'message': r.text}


@router.get('/popular/', status_code=200)
async def popular():
    return {
        'message': [
            'BillGates',
            'realDonaldTrump',
            'elonmusk',
            'iamdevloper',
        ]
    }

