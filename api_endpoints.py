from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from icds.data import list_repos, list_commits, get_repo_name_by_id

from db_engine import get_db_session

app = FastAPI(
    title="FastAPI with Jinja2 Templates",
    description="This is a simple example of FastAPI with Jinja2 templates",
    version="0.1.0",
)
db = next(get_db_session())


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
    return templates.TemplateResponse(request=request, name="home.html", context={})


@app.get("/repos")
async def get_repos():
    result = list_repos(db, 5)
    return result


@app.get("/repos/{repo_id}", response_class=HTMLResponse)
async def show_more_info(request: Request, repo_id: str):
    commits = list_commits(db=db, repo_id=repo_id, limit=5)
    repo_name = get_repo_name_by_id(db=db, repo_id=repo_id)
    return templates.TemplateResponse(
        request=request,
        name="repoInfo.html",
        context={
            "repo_name": repo_name,
            "commits": commits,
        },
    )
