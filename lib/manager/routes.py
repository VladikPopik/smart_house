from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.conf import config
from lib.manager.auth import auth_router

app = FastAPI(openapi_url="/openapi.json", docs_url="/docs")

origins = [
    f"{config.ssl_conn.PROTOCOL}://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
