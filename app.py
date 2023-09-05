from flask import Flask, jsonify, request
from tasks import run_sherlock_task, run_holehe_task
from flask_caching import Cache


app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/api/sherlock', methods=['POST'])
def run_sherlock():
    username = request.json.get('username')
    cached_result = cache.get(username)

    if cached_result:
        return jsonify({"result": cached_result})

    task = run_sherlock_task.apply_async(args=[username])
    return jsonify({"task_id": task.id}), 202

@app.route('/api/sherlock/status/<task_id>', methods=['GET'])
def sherlock_status(task_id):
    task = run_sherlock_task.AsyncResult(task_id)
    return jsonify({"status": task.status, "result": task.result if task.successful() else None})

@app.route('/api/holehe', methods=['POST'])
def run_holehe():
    email = request.json.get('email')
    cached_result = cache.get(email)

    if cached_result:
        return jsonify({"result": cached_result})

    task = run_holehe_task.apply_async(args=[email])
    return jsonify({"task_id": task.id}), 202

@app.route('/api/holehe/status/<task_id>', methods=['GET'])
def holehe_status(task_id):
    task = run_holehe_task.AsyncResult(task_id)
    return jsonify({"status": task.status, "result": task.result if task.successful() else None})

if __name__ == '__main__':
    app.run(debug=True)
