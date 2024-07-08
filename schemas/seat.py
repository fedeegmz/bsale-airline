# SQLAlchemy
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String
)

# database
from database.mysql_client import meta


SeatTable = Table(
    "seat",
    meta,
    Column(
        "seat_id",
        Integer,
        primary_key = True
    ),
    Column(
        "seat_column",
        String(2)
    ),
    Column(
        "seat_row",
        Integer
    ),
    Column(
        "seat_type_id",
        Integer
    ),
    Column(
        "airplane_id",
        Integer
    )
)
