// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Order = { customer: string; amountCents: number };

export function grandTotal(orders: Order[]): number {
  return orders.reduce((sum, order) => sum + order.amountCents, 0);
}

export function totalsByCustomer(orders: Order[]): Map<string, number> {
  return orders.reduce((totals, order) => {
    totals.set(order.customer, (totals.get(order.customer) ?? 0) + order.amountCents);
    return totals;
  }, new Map<string, number>());
}
