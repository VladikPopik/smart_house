from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CONFIG_PROTOCOL, CONFIG_HOST_ORIGIN, CONFIG_PORT

app = FastAPI(openapi_url="/openapi.json", docs_url="/docs")

origins = [
    f"{CONFIG_PROTOCOL}://{CONFIG_HOST_ORIGIN}:{CONFIG_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# app.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["auth"],
# )
