from example import app, template
from fastapi import Request

@app.get("/")
async def index(request: Request):
    return template.TemplateResponse('index.html', {'request': request}) 


@app.get("/tutorial")
async def tutorial():
    """ This is a tutorial function to use this run curl http://0.0.0.0:5700/tutorial """
    return {"message": {"This is another route"}}
