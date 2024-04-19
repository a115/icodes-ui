
import uvicorn
if __name__ == "__main__":
    uvicorn.run("api_endpoints:app", reload=True, reload_dirs=["."])
