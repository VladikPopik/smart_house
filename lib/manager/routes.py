from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.conf import config
from lib.manager.auth import auth_router
from lib.manager.monthly_plan import plan_router
from lib.manager.monitoring import monitoring_router_ws
from lib.manager.motion import motion_ws_router
from lib.manager.settingsd import settings_router


app = FastAPI(openapi_url="/openapi.json", docs_url="/docs")

origins = [
    f"{config.ssl_conn.PROTOCOL}://{config.origins.host}:{config.origins.port}",
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

app.include_router(plan_router, prefix="/budget", tags=["budget"])

app.include_router(
    monitoring_router_ws,
    prefix="/mon_ws",
    tags=["mon_ws"],
)
app.include_router(motion_ws_router, prefix="/motion_ws", tags=["motions_ws"])

app.include_router(settings_router, prefix="/settings", tags=["settings"])
