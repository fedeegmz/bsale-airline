# FastAPI
from fastapi import FastAPI, Path
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

# db
from db import cursor

# models
from models import *


app = FastAPI()

@app.get("/")
async def root():
    sql = "SELECT * FROM passenger LIMIT 10"
    cursor.execute(sql)
    results = cursor.fetchall()

    return {"testData": jsonable_encoder(results)}


@app.get(
    path = "/checkin"
)
async def check_in(
    id: str = Path(...)
):
    pass