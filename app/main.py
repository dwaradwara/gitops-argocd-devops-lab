import os
from fastapi import FastAPI

app = FastAPI(title="TBC GitOps Lab")

APP_VERSION = os.getenv("APP_VERSION", "v1")
APP_MESSAGE = os.getenv("APP_MESSAGE", "GitOps application running")


@app.get("/")
def root():
    return {
        "application": "tbc-gitops-api",
        "version": APP_VERSION,
        "message": APP_MESSAGE
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": APP_VERSION
    }
