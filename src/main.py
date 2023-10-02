# src/main.py

# import builtins
import validators

# import external libraries
from fastapi import FastAPI

# import local libraries
from . import schema


app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the URL shortner API..."

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url: schema.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(mesasge="Your provided URL is not a valid URL")
    return f"TODO: Create database entry for: {url.target_url}"

