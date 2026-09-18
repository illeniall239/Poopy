import pandas as pd


def enrich_orders(orders: pd.DataFrame, customers: pd.DataFrame, how: str = "inner") -> pd.DataFrame:
    """Merge customer name and country onto orders by customer_id (inner or left); ValueError otherwise."""
    raise NotImplementedError


def orders_per_customer(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.Series:
    """Integer order count per customer in customers' order, 0 for customers with no orders."""
    raise NotImplementedError
