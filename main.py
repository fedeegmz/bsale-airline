# FastAPI
from fastapi import FastAPI

# routers
from routers import check_in


app = FastAPI()
app.include_router(check_in.router)


@app.get(
    path = "/",
    include_in_schema = False
)
async def root():
    return {"msg": "API works"}
    # return {"url": "https://checkinairline-1-s8126205.deta.app/flights/1/passengers"}
