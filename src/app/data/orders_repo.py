"""Data layer. Only the service layer may import this module."""

_ORDERS = {1: {"id": 1, "total": 42.0}}


def get(order_id: int) -> dict | None:
    return _ORDERS.get(order_id)
