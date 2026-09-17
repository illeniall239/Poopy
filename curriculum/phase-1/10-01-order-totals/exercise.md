# Order totals

Topic: 10. Higher-order functions and closures
Difficulty: 1 of 3

## Problem

A shop exports its orders as a list of `Order` objects: `{ customer: string; amountCents: number }`. Amounts are whole cents, so there are no floating-point surprises.

Write two functions, using `reduce` instead of loops:

- `grandTotal(orders)` returns the sum of every `amountCents`. An empty list totals `0`.
- `totalsByCustomer(orders)` returns a `Map<string, number>` from each customer name to the sum of their orders. Customer names are case-sensitive. The Map's keys are in the order each customer first appears in `orders`. An empty list gives an empty Map.

Neither function may change the `orders` array or the objects in it.

## Examples

```
const orders = [
  { customer: "ana", amountCents: 1200 },
  { customer: "ben", amountCents: 500 },
  { customer: "ana", amountCents: 300 },
];

grandTotal(orders)        → 2000
grandTotal([])            → 0
totalsByCustomer(orders)  → Map { "ana" → 1500, "ben" → 500 }
totalsByCustomer([])      → Map {}
```

## Constraints

- `orders` has 0 to 10000 items.
- `amountCents` is a whole number from 0 to 1000000.
- Use `reduce`, not `for`, `while` or `forEach`.

## Hints

1. With a loop, what variable would you create before the loop, and what would you do to it for each order? Which parts of a `reduce` call play those two roles?
2. What does `reduce` do with an empty array when you give it no starting value? Try it in the console.
3. For `totalsByCustomer`, the thing you carry from one order to the next isn't a number. What should it start as, and what must the callback give back at the end of every step?
4. When a customer isn't in the Map yet, what does `get` return? How can you turn that into a number you can add to?

## Explain-back

- What is `reduce`'s second argument for, and what happens in `grandTotal([])` if you leave it out?
- Why must your `totalsByCustomer` callback return the Map on every step, even though it's the same Map each time?
- Someone writes `let total = 0; orders.map(o => total += o.amountCents)`. It gives the right total. What's wrong with using `map` this way?
