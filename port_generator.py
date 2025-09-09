
import os
import socket

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
WEB_PATH = os.getenv("WEB_PATH")

if LOGIN is None \
        or PASSWORD is None \
        or WEB_PATH is None:
    raise Exception("Missing environment variables")


class LoginPayload(BaseModel):
    username: str
    password: str


app = FastAPI(docs_url="/docs",
              redoc_url="/api/redoc",
              openapi_url="/api/openapi.json",
              swagger_ui_parameters={
                  "tryItOutEnabled": True,
              })


@app.post(f"/{WEB_PATH}/")
async def get_free_port(login_payload: LoginPayload) -> int:
    if login_payload.username != LOGIN or login_payload.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return int(s.getsockname()[1])
