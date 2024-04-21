from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi import FastAPI, Request


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
    return templates.TemplateResponse(request=request, name="home.html", context={})


@app.get("/get-repos")
async def get_repos():
    return [
        {
            "id": "some_id",
            "name": "some_name",
            "path": "some/path/to/repo",
            "remote_url": "some_remote_url",
            "description": "some_description",
        },
        {
            "id": "some_id_1",
            "name": "some_name_1",
            "path": "some/path/to/repo_1",
            "remote_url": "some_remote_url_1",
            "description": "some_description_1",
        },
    ]


@app.get("/show-more-info/{repo_id}", response_class=HTMLResponse)
async def get_another_page(request: Request):
    # logic to get more info about the repo
    sample_commit_details_for_repo = [
        {
            "id": "some_commit_id",
            "repo_id": "some_repo_id",
            "hash": "1c1afa26098f1252018dc15ef7a0af09c6195a43",
            "datetime": datetime.now(),
            "author": "John Smith",
            "commit_message": "Makes OPENAI_API_KEY required",
            "file_stats": """M README.md
M icds/settings.py
M pyproject.toml""",  # could be very long string
            "summary": "Makes OPENAI_API_KEY required",  # very long string
            "details": """
Key changes in the commit:
1. Updated the README.md file to include instructions on setting environment variables for the OpenAI API key and the default model to be used.
2. Modified the icodes/settings.py file to remove the default empty value for OPENAI_API_KEY.
3. Updated the version number in the pyproject.toml file from "0.1.1" to "0.1.3".

Inference of intent:
1. The changes indicate a focus on enhancing the installation and configuration process for the iCODES application, specifically related to setting up the OpenAI API key and specifying the default GPT model to use.
2. By removing the default empty value for OPENAI_API_KEY in the settings file, the intention seems to enforce the requirement of users providing their API key, emphasizing the necessity for this configuration.
3. Updating the version number in pyproject.toml suggests that new features or improvements have been made to the application since the previous version "0.1.1", signalling a progression in the development of the tool.

Overall, the intent behind the changes appears to be improving user experience, ensuring proper configuration, and advancing the functionality of the iCODES application.
""",  # very long string
        },
        {
            "id": "some_commit_id_1",
            "repo_id": "some_repo_id_1",
            "hash": "8f716eeb2490904ac148f49720ddbef080562c69",
            "datetime": datetime.now(),
            "author": "Jane Doe",
            "commit_message": "Feat/staged commit message suggestions (#14)",
            "file_stats": """
M README.md
M icds/git_helpers.py
M icodes.py
""",  # could be very long string
            "summary": "Feat/staged commit message suggestions (#14)",  # very long string
            "details": """
Key Changes:
1. Modified README.md:
   - Updated instances of "analyze" to "analyse" for consistency.
   - Changed "analyze" to "analyse" for clarity in describing what iCODES does.
   - Added a section for suggesting a commit message based on currently staged changes.

2. Modified icds/git_helpers.py:
   - Added `format_change_diff`, `format_change_str`, and `get_staged_changes` functions for better organization and readability.
   - Refactored `extract_commit_info` to use `format_change_diff` for improved output formatting.
   - Added `CHANGE_TYPES` dictionary for mapping change types.
   - Added `should_ignore_change` function for determining if a change should be ignored.
   - Implemented handling of ignored changes based on filenames.
   - Updated the output format to include change types in a more descriptive manner.

3. Modified icodes.py:
   - Added `get_staged_changes` function for retrieving formatted staged changes.
   - Updated `inspect_repo` and `build_index` commands to use type hints and provide user-friendly help messages.
   - Added a new `suggest_commit_message` command to suggest a commit message based on staged changes.
   - Utilized `get_staged_changes` and `analyse_commit` functions to suggest a commit message and display analysis.

Intent behind the Changes:
1. The intent was to standardize the language in the README and improve clarity for users by using "analyse" consistently. Additionally, the addition of the section for suggesting a commit message aims to enhance workflow efficiency by providing a convenient feature for users.

2. The changes in `git_helpers.py` suggest a focus on improving code readability, maintainability, and extensibility. By introducing new functions and enhancing existing ones, the code becomes more modular, making it easier to manage different aspects of change handling.

3. The modifications in `icodes.py` reflect a desire to enhance user experience by adding functionality to suggest commit messages based on staged changes. This feature aims to streamline the commit process and provide users with helpful insights into their changes before creating a commit. Additionally, the updates to command signatures and help messages aim to improve usability and clarity for users interacting with the CLI tool.
""",  # very long string
        },
    ]
    return templates.TemplateResponse(
        request=request,
        name="repoInfo.html",
        context={
            "repo_name": "some_repo_name",
            "commits": sample_commit_details_for_repo,
        },
    )
