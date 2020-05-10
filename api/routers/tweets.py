from fastapi import APIRouter, Response
from textblob import TextBlob
import requests, os, json
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Tweet(BaseModel):
  id_str: str
  created_at: str
  text: str
  has_media: bool
  hashtags: List[str]
  user_mentions: List[str]
  retweet_count: int
  favorite_count: int
  # is_quote_status: bool


def get_tweets(screen_name, max_id=None, since_id=None, count=200):
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
  }

  base = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
  params = 'tweet_mode=extended&trim_user=true&retweeted=false'
  params += f'&screen_name={screen_name}'
  params += f'&count={count}'
  
  if max_id != None:
    params += f'&max_id={max_id}'
  elif since_id != None:
    params += f'since_id={since_id}'

  return requests.get(f'{base}?{params}', headers=headers)

@router.get('/', status_code=200)
def tweets(screen_name, response: Response, count=200):
  r = get_tweets(screen_name)
  if r.status_code != 200:
    response.status_code = 401
    return {'message': 'nope'}

  return {'message': r.text}


@router.get('/analyze/', status_code=200)
def analyze_tweets(screen_name, response: Response, count=200):
  r = get_tweets(screen_name)
  
  if r.status_code != 200:
    response.status_code = 401
    return {'message': 'nope'}
  parsed = json.loads(r.text)
  for tweet in parsed:
      text = tweet['full_text']
      blob = TextBlob(text)
      tweet['polarity'], tweet['subjectivity'] = blob.sentiment

  return {'message': json.dumps(parsed)}