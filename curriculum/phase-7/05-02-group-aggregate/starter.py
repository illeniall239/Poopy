import pandas as pd


def revenue_by_region(orders: pd.DataFrame) -> pd.DataFrame:
    """Paid orders only: per region count, revenue and mean order value, sorted by revenue descending."""
    raise NotImplementedError


def share_by_status(orders: pd.DataFrame) -> pd.Series:
    """Fraction of all orders per status, descending."""
    raise NotImplementedError
