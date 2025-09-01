

from fastapi import FastAPI, HTTPException
import socket
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

LOGIN = os.getenv("PANEL_LOGIN")
PASSWORD = os.getenv("PANEL_PASSWORD")


class LoginPayload(BaseModel):
    username: str
    password: str


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc",
              openapi_url="/api/openapi.json")


@app.get("/")
async def get_free_port(login_payload: LoginPayload) -> int:
    if login_payload.username != LOGIN or login_payload.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return int(s.getsockname()[1])
