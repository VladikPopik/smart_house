from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(openapi_url='/openapi.json', docs_url='/docs')
