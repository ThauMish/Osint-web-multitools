from celery import Celery
from flask_caching import Cache
import redis
import subprocess

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
SHERLOCK_PATH = '/root/project/sherlock/sherlock/sherlock.py'
redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)

@app.task
def run_sherlock_task(username):
    cached_result = redis_client.get(username)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['python3', SHERLOCK_PATH, username], capture_output=True, text=True)
    redis_client.set(username, result.stdout)
    return result.stdout

@app.task
def run_holehe_task(email):
    cached_result = redis_client.get(email)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['holehe', email], capture_output=True, text=True)
    redis_client.set(email, result.stdout)
    return result.stdout






    