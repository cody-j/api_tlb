from fastapi import APIRouter, Response
import requests
import os

router = APIRouter()

@router.get('/', status_code=200)
def get_tweets(screen_name, response: Response, count=200):
  headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
  }

  base = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
  params = f'screen_name={screen_name}&count={count}&tweet_mode=extended&trim_user=true&retweeted=false'

  r = requests.get(f'{base}?{params}', headers=headers)
  

  
  if r.status_code != 200:
      response.status_code = 401
      return {'message': 'nope'}

  return {'message': r.text}
