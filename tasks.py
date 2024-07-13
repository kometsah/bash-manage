from celery import Celery
import docker

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def run_bash_script(container_name, script):
    client = docker.from_env()
    container = client.containers.get(container_name)
    exec_log = container.exec_run(f'bash -c "{script}"', stdout=True, stderr=True)
    return exec_log.output.decode('utf-8')
