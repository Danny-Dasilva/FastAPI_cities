from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory='./example/static'), name="static")

template = Jinja2Templates(directory='./example/templates')

from example.views import main, tasks
