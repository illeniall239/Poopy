# Shipping cost

Topic: 3. Conditionals and boolean logic
Difficulty: 2 of 3

## Problem

An online shop charges shipping by these rules:

- **Free shipping:** orders with a subtotal of 5000 cents or more ship for free, but only if they are not express and weigh 20 kg or less.
- **Standard price by weight:** up to and including 1 kg costs 499 cents; over 1 kg up to and including 5 kg costs 899 cents; over 5 kg costs 1499 cents.
- **Express:** adds 1000 cents to the standard price. Express orders never ship for free.
- **Too heavy:** orders over 30 kg can't be shipped at all.

Write `shippingCost(subtotalCents, weightKg, express)` that returns the shipping cost in cents, or `-1` if the order can't be shipped.

The rules are listed in the order a customer reads them, not necessarily the order your code should check them.

## Examples

```
shippingCost(2000, 1, false)   → 499
shippingCost(2000, 1.5, false) → 899
shippingCost(6000, 3, false)   → 0
shippingCost(6000, 3, true)    → 1899
shippingCost(6000, 25, false)  → 1499
shippingCost(9000, 31, false)  → -1
```

## Constraints

- `subtotalCents` is a whole number from 0 to 10000000.
- `weightKg` is a number greater than 0 and at most 1000; it may have decimals.
- `express` is `true` or `false`.

## Hints

1. Put each example through the rules by hand. For which examples does more than one rule seem to apply?
2. A 31 kg order with a big subtotal matches both "free shipping" and "too heavy". Which answer is right, so which rule must your code check first?
3. The weight tiers overlap too: a 0.5 kg parcel is also "5 kg or less". If you check the tiers from lightest to heaviest, which comparison should each one use? What if you check from heaviest to lightest?
4. Write the free-shipping condition as one boolean expression with three parts joined by `&&`. Which weights and subtotals sit exactly on a boundary, and does your expression treat them the way the rules say?

## Explain-back

- Which rule does your code check first, and what would break if it came last?
- What does your code return for exactly 5 kg, and which comparison operator decides that?
- "Not (express or over 20 kg)" is one way to say who gets free shipping. Say the same thing without the outer "not". Is it the same?
