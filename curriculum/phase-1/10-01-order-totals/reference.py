# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from dataclasses import dataclass
from functools import reduce


@dataclass
class Order:
    customer: str
    amount_cents: int


def grand_total(orders: list[Order]) -> int:
    return reduce(lambda total, order: total + order.amount_cents, orders, 0)


def totals_by_customer(orders: list[Order]) -> dict[str, int]:
    def add(totals: dict[str, int], order: Order) -> dict[str, int]:
        totals[order.customer] = totals.get(order.customer, 0) + order.amount_cents
        return totals

    return reduce(add, orders, {})
