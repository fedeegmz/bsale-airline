# SQLAlchemy
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String
)

# database
from database.mysql_client import meta


SeatTypeTable = Table(
    "seat_type",
    meta,
    Column(
        "seat_type_id",
        Integer,
        primary_key = True
    ),
    Column(
        "name",
        String(255)
    )
)
