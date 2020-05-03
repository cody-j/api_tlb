import os, requests
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from .routers import tweets, user

# load environment (this dir)
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET'],
    allow_headers=['*']
)

# routers
app.include_router(tweets.router, prefix='/tweets')
app.include_router(user.router, prefix='/user')

# health check
@app.get('/')
async def root(status_code=200):
    return {'message': 'healthy'}
