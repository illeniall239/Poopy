# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import pandas as pd


def revenue_by_region(orders: pd.DataFrame) -> pd.DataFrame:
    return (
        orders[orders["status"] == "paid"]
        .groupby("region")
        .agg(orders=("amount", "count"), revenue=("amount", "sum"), mean_order=("amount", "mean"))
        .sort_values("revenue", ascending=False)
    )


def share_by_status(orders: pd.DataFrame) -> pd.Series:
    return orders["status"].value_counts(normalize=True)
