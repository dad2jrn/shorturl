# src/main.py

# import builtins
import validators
import secrets

# import external libraries
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# import local libraries


from . import schema, models
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return "Welcome to the URL shortner API..."

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url", response_model=schema.URLInfo)
def create_url(url: schema.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
