from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"id": id}
    )

@app.get("/another-task", response_class=HTMLResponse)
async def get_another_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="anotherPage.html", context={}
    )