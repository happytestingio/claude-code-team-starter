"""API layer. Calls the service layer, never the data layer (see CLAUDE.md, rule R1)."""
from src.app import orders_service


def get_order_total(order_id: int) -> dict:
    return {"id": order_id, "total": orders_service.order_total(order_id)}
