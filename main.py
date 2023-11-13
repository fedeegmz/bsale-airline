# FastAPI
from fastapi import FastAPI

# security
from security.config import settings

# routers
from routers.flights import router


app = FastAPI(
    title = settings.app_name.title(),
    version = "0.2",
    contact = {"admin": settings.admin_email},
    summary = ""
)
app.include_router(router)


@app.get(
    path = "/",
    include_in_schema = False
)
async def root():
    return {"msg": "API works"}
    # return {"url": "https://checkinairline-1-s8126205.deta.app/flights/1/passengers"}
