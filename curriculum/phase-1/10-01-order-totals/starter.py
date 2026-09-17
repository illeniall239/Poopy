from dataclasses import dataclass


@dataclass
class Order:
    customer: str
    amount_cents: int


def grand_total(orders: list[Order]) -> int:
    """Return the sum of every order's amount_cents."""
    raise NotImplementedError


def totals_by_customer(orders: list[Order]) -> dict[str, int]:
    """Return {customer: total cents} in order of each customer's first appearance."""
    raise NotImplementedError
