export type Order = { customer: string; amountCents: number };

export function grandTotal(orders: Order[]): number {
  throw new Error("Not implemented");
}

export function totalsByCustomer(orders: Order[]): Map<string, number> {
  throw new Error("Not implemented");
}
