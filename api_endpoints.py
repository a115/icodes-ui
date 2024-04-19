from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from icds.data import get_repo_by_name
from icds import models
from sqlmodel import Session

app = FastAPI(
    title="FastAPI with Jinja2 Templates",
    description="This is a simple example of FastAPI with Jinja2 templates",
    version="0.1.0",

)

# Add CORS middleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={}
    )


@app.get("/get-repo/{repo_name}")
async def get_repos(repo_name: str, db: Session = Depends(models.get_db)):  # extract db out of the request
    res = get_repo_by_name(db, repo_name)
    if res:
        return {
            "repo_name": res.name,
            "repo_path": res.path,
            "remote_url": res.remote_url,
        }
    return {"message": "Repo not found"}


@app.get("/another-task", response_class=HTMLResponse)
async def get_another_page(request: Request):
    # data.get_repo_name_by_id()
    return templates.TemplateResponse(
        request=request, name="anotherPage.html", context={}
    )
