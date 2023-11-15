# FastAPI
from fastapi import APIRouter, Path
from fastapi import HTTPException, status

# database
from database.mysql_client import conn

# schemas
from schemas.flight import flight

# models
from models.response.model import ResponseModel
from models.flight_data import FlightData


router = APIRouter(
    prefix = "/flights"
)

### PATH OPERATIONS ###

@router.get(
    path = "/{flight_id}/passengers",
    status_code = status.HTTP_200_OK,
    # response_model = ResponseModel,
    summary = "Returns the check-in data",
    tags = ["check-in"]
)
async def check_in(
    flight_id: str = Path(...)
):
    if not flight_id in ("1", "2", "3", "4"):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "code": 400,
                "errors": "incorrect flight id"
            }
        )
    
    result = conn.execute(flight.select().where(flight.c.flight_id == flight_id)).first()
    flight_data = FlightData(*result)

    return flight_data.model_dump(by_alias=True)
