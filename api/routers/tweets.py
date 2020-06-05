from fastapi import APIRouter, Response
from textblob import TextBlob
import requests, os, json, urllib.parse
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
  params = {
    'tweet_mode': 'extended',
    'screen_name': screen_name,
    'trim_user': True,
    'include_rts': True,
    'count': count
  }
  params = urllib.parse.urlencode(params)
  
  if max_id != None:
    params += f'&max_id={max_id}'
  elif since_id != None:
    params += f'since_id={since_id}'

  return requests.get(f'{base}?{params}', headers=headers)

@router.get('/', status_code=200)
def tweets(screen_name, response: Response, count=200, analyze=False, max_id=None):
  r = get_tweets(screen_name, count=count, max_id=max_id)
  if r.status_code != 200:
    response.status_code = 401
    return {'message': 'nope'}

  tweets = json.loads(r.text)
  if analyze:
    for tweet in tweets:
        text = tweet['retweeted_status']['full_text'] if tweet['retweeted_status'] else tweet['full_text']
        blob = TextBlob(text)
        tweet['polarity'], tweet['subjectivity'] = blob.sentiment
  
  return {'message': json.dumps(tweets)}


@router.get('/analyze/', status_code=200)
def analyze_tweets(screen_name, response: Response, count=200):
  r = get_tweets(screen_name, count=count)
  
  if r.status_code != 200:
    response.status_code = 401
    return {'message': 'nope'}
  parsed = json.loads(r.text)
  for tweet in parsed:
    text = tweet['full_text']
    blob = TextBlob(text)
    tweet['polarity'], tweet['subjectivity'] = blob.sentiment

  return {'message': json.dumps(parsed)}\
  
@router.get('/search/', status_code=200)
def search_tweets(query, response: Response, count=200, analyze=False):
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {os.getenv("AUTH_KEY")}'
  }
  print('query: ', query)
  base = 'https://api.twitter.com/1.1/search/tweets.json'
  params = {
    'tweet_mode': 'extended',
    'q': '"' + query + '"',
    'count': count
  }
  params = urllib.parse.urlencode(params)
  r = requests.get(f'{base}?{params}', headers=headers)
  if r.status_code != 200:
    response.status_code = 401
    return {'message': 'nope'}
  
  tweets = json.loads(r.text)['statuses']
  
  if analyze:
    for tweet in tweets:
      text = tweet['full_text']
      blob = TextBlob(text)
      tweet['polarity'], tweet['subjectivity'] = blob.sentiment
  
  return {'message': json.dumps(tweets)}
