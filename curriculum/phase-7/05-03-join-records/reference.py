# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import pandas as pd


def enrich_orders(orders: pd.DataFrame, customers: pd.DataFrame, how: str = "inner") -> pd.DataFrame:
    if how not in ("inner", "left"):
        raise ValueError("how must be 'inner' or 'left'")
    return pd.merge(orders, customers[["customer_id", "name", "country"]], on="customer_id", how=how).reset_index(drop=True)


def orders_per_customer(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.Series:
    counts = orders.groupby("customer_id").size()
    return counts.reindex(customers["customer_id"]).fillna(0).astype(int)
