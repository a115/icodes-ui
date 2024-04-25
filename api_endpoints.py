from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from icds.data import get_repo_by_name, get_db_commit_by_hash

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


@app.get("/get-repos")
async def get_repos():
    result = get_repo_by_name(db, "iCODES")
    return [result]


@app.get("/show-more-info/{repo_id}", response_class=HTMLResponse)
async def get_another_page(request: Request):
    commit = get_db_commit_by_hash(db, "1c1afa26098f1252018dc15ef7a0af09c6195a43")
    return templates.TemplateResponse(
        request=request,
        name="repoInfo.html",
        context={
            "repo_name": "some_repo_name",
            "commits": [commit],
        },
    )
