from celery import Celery
from flask_caching import Cache
import redis
import subprocess

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
SHERLOCK_PATH = '/root/project/sherlock/sherlock/sherlock.py'
DAPROFILER_PATH = '/root/project/DaProfiler/profiler.py'
redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)

@app.task
def run_sherlock_task(username):
    cache_key = f'holehe-{username}'
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['python3', SHERLOCK_PATH, username], capture_output=True, text=True)
    redis_client.set(username, result.stdout)
    return result.stdout

@app.task
def run_holehe_task(email):
    cache_key = f'holehe-{email}'
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['holehe', email], capture_output=True, text=True)
    redis_client.set(email, result.stdout)
    return result.stdout

@app.task
def run_daprofiler_task(first_name, last_name):
    cache_key = f'daprofiler-{first_name}-{last_name}'
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['python3', DAPROFILER_PATH, '-n', first_name, '-ln',  last_name], capture_output=True, text=True)
    redis_client.set(cache_key, result.stdout)
    return result.stdout

@app.task
def run_maigret_task(username):
    cache_key = f'maigret-{username}'
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result.decode('utf-8')
    
    result = subprocess.run(['maigret', username, '--timeout 3'], capture_output=True, text=True)
    redis_client.set(cache_key, result.stdout)
    return result.stdout
