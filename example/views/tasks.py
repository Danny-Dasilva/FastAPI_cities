from datetime import datetime
from time import sleep

from fastapi import BackgroundTasks, Request, status
from fastapi.responses import JSONResponse

from example import app, template

def _run_task(name: str, id=None):
    sleep(3)
    with open("./example/tasks_out.txt", mode="a") as file:
        now = datetime.now()
        content = f"{name} [{id}]: {now}\n"
        file.write(content)


@app.post("/task/run/{name}/{id}")
async def task_run(name: str, id:int, background_tasks: BackgroundTasks):
    """ takes in a tasks and write it into a file"""
    background_tasks.add_task(_run_task, name, id)
    return {"message": f"Task : {name} ID {id} is being run\n"}
