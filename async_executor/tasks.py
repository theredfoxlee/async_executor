import subprocess
import time

from .models import Task

from . import dramatiq


@dramatiq.actor
def execute(task_name, args, cwd=None, timeout=None, hosts=None):
    """ executes command on the dramatiq worker """
    task = Task.get_by(name=task_name)
    task.update_status('SENT')
    start = time.time()
    try:
        completed_process = subprocess.run(
            args=args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            timeout=float(timeout) if timeout else None
        )
        elapsed = time.time() - start
        task.update_done(
            returncode=completed_process.returncode,
            stdout=completed_process.stdout,
            stderr=completed_process.stderr,
            duration=elapsed
        )
    except subprocess.TimeoutExpired:
        task.update_status('Timeouted')
    except FileNotFoundError:
        task.update_status('FileNotFound')
