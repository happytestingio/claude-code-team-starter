"""Service layer: the only code that talks to the data layer."""
from src.app.data import orders_repo


def order_total(order_id: int) -> float:
    order = orders_repo.get(order_id)
    if order is None:
        raise KeyError(order_id)
    return order["total"]
