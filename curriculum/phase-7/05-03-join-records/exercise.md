# Join records

Topic: 5. pandas DataFrames and loading data
Difficulty: 2 of 3

## Problem

`orders` has columns `order_id`, `customer_id`, `amount`. `customers` has columns `customer_id`, `name`, `country`, with one row per customer. Write two functions with pandas (required):

- `enrich_orders(orders: pd.DataFrame, customers: pd.DataFrame, how: str = "inner") -> pd.DataFrame` — `pd.merge` on `customer_id` with `how` either `"inner"` or `"left"` (raise `ValueError` for anything else). The result has the order columns followed by `name` and `country`, keeps the orders' row order, and has a fresh `0..n-1` index. With `"left"`, orders whose customer is unknown keep their row with `NaN` in `name` and `country`; with `"inner"` they are dropped.
- `orders_per_customer(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.Series` — number of orders for every customer in `customers`, indexed by `customer_id` in the customers' order, with `0` (an integer) for customers who never ordered. Orders whose customer is not in `customers` are ignored.

Neither function modifies its inputs.

## Examples

```
orders                          customers
 order_id customer_id amount     customer_id name country
        1           7    10.0              7  Ann      NO
        2           7    20.0              8  Bob      DE
        3           9     5.0              9  Cy       FR
        4          42    99.0

enrich_orders(orders, customers)            → 3 rows: orders 1, 2, 3 with name/country; order 4 dropped
enrich_orders(orders, customers, "left")    → 4 rows: order 4 has NaN name and country
orders_per_customer(orders, customers)      → 7: 2, 8: 0, 9: 1
```

## Constraints

- Up to 100 000 orders and 10 000 customers.
- A customer appearing twice in `customers` is a one-to-many join and would duplicate orders; the test shows it and expects the duplication (that is what `merge` does).
- Compared with `pandas.testing`.

## Hints

1. Which `pd.merge` arguments name the key column and the join type? What does the result's index look like right after a merge?
2. With `how="left"`, what fills `name` for a `customer_id` that is missing from `customers`? Which dtype does the column get?
3. `orders_per_customer` needs a zero for customers who never ordered. Would `groupby("customer_id").size()` alone have a row for them? Which method aligns a Series to a given index and fills the gaps?
4. If the count column becomes float after filling, what did the fill introduce, and how do you get integers back?

## Explain-back

- An inner join of 1 000 orders with a customers table returned 1 300 rows. Whose fault is that, and how would you find the offending keys?
- What is the difference between the rows kept by an inner, a left and an outer join here? Which would you choose for "revenue per country, including orders with unknown customers"?
- `orders.merge(customers)` without `on=` worked in a notebook. What did pandas join on, and why is that fragile?
- Why does `reindex(customers.customer_id)` followed by `fillna(0)` produce a float Series, and why should a count column be integer?
