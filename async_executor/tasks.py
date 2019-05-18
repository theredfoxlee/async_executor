import subprocess
#import dramatiq
import time

from .models import Task

from . import dramatiq


@dramatiq.actor
def execute(task_name, args, cwd=None):
    """ executes command on the dramatiq worker """
    task = Task.get_by(name=task_name)
    task.update_status('SENT')
    start = time.time()
    completed_process = subprocess.run(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
    )
    elapsed = time.time() - start
    task.update_done(
        returncode=completed_process.returncode,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        duration=elapsed
    )
