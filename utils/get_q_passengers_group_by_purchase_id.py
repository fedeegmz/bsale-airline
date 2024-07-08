# SQLAlchemy
from sqlalchemy import text

# database
from database.mysql_client import conn


def get_q_passengers_group_by_purchase_id(fligth_id: int):
    query = f'select count(*) as quantity, bp.purchase_id '\
            f'from airline.boarding_pass as bp '\
            f'where bp.flight_id = {fligth_id} '\
            f'group by bp.purchase_id '\
            f'having quantity = 1 '\
            f'order by quantity desc;'
    data = conn.execute(
        text(query)
    ).all()

    list_to_return = []
    for item in data:
        list_to_return.append(item[1])
    return list_to_return
