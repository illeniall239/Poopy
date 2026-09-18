# Group and aggregate

Topic: 5. pandas DataFrames and loading data
Difficulty: 2 of 3

## Problem

`orders` is a DataFrame with columns `order_id`, `region`, `status` and `amount`. Write two functions with pandas (required):

- `revenue_by_region(orders: pd.DataFrame) -> pd.DataFrame` — keep only rows whose `status` is `"paid"`, group by `region` and return one row per region with columns `orders` (count), `revenue` (sum of `amount`) and `mean_order` (mean of `amount`), sorted by `revenue` descending. `region` is the index of the result. Rows whose `region` is missing are dropped, which is what `groupby` does by default.
- `share_by_status(orders: pd.DataFrame) -> pd.Series` — the fraction of all orders in each status (`value_counts(normalize=True)`), indexed by status, sorted descending by share. Uses every row, not only paid ones.

Neither function modifies `orders`. Build each as a chain of filter, groupby, aggregate and sort; no row loops.

## Examples

```
orders:
   order_id region status  amount
0         1  north   paid    10.0
1         2  north   paid    30.0
2         3  south   paid     5.0
3         4  south refund    50.0
4         5    NaN   paid   100.0

revenue_by_region(orders)
        orders  revenue  mean_order
region
north        2     40.0        20.0
south        1      5.0         5.0

share_by_status(orders)
paid      0.8
refund    0.2
```

## Constraints

- Up to 100 000 rows.
- Column names and order of the result are exactly `orders`, `revenue`, `mean_order`; the index is named `region`.
- Compared with `pandas.testing.assert_frame_equal` / `assert_series_equal` (with a tolerance; integer vs float dtypes for `orders` are both accepted).

## Hints

1. Which expression gives a boolean Series marking paid rows, and how do you use it to select only those rows?
2. `groupby("region")` returns a grouper. Which method lets you compute several named aggregates in one call (`orders=("amount", "count")` style)?
3. The example has an order with `region` `NaN`. Count the rows in the result: what happened to it, and which `groupby` argument would change that?
4. `value_counts` on the `status` column already counts. Which argument turns counts into fractions?

## Explain-back

- `orders[orders.status == "paid"]` was evaluated in a notebook and `orders` still contains refunds. Why? What would you write to keep only paid rows in `orders` itself?
- `groupby` silently dropped the `NaN` region and 100.0 of revenue with it. In an analysis, when is that acceptable and when must you use `dropna=False` and report the "unknown" group?
- Write the `revenue_by_region` chain as a sentence describing what happens to a single row from the input as it flows through.
- Someone computes `mean_order` with `.apply(lambda g: g.amount.mean())`. Why is the named aggregation faster, and what does "vectorized" mean here?
