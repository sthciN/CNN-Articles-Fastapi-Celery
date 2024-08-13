from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv
from celery import Celery
import redis

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = FastAPI()

# Initialize the Redis object
redis_url = "redis://localhost:6379/0"
broker = redis.Redis.from_url(redis_url)

# Configure Celery to use the redis message broker
celery_app = Celery('tasks', broker=redis_url, backend=redis_url)