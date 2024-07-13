from flask import Flask, request, jsonify
from tasks import run_bash_script

app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def schedule_script():
    data = request.get_json()
    container_name = data.get('container_name')
    script = data.get('script')
    schedule_time = data.get('schedule_time')  # e.g., "2024-07-15T10:00:00"

    task = run_bash_script.apply_async((container_name, script), eta=schedule_time)
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
