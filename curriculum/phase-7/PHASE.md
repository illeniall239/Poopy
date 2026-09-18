# Phase 7 — Data and math for machine learning

About 90 hours over about 7 weeks, 14 Topics. For a Learner who has finished the DSA and full-stack phases and knows Python syntax but has never used the Python data stack. At the end the Learner can load, clean and explore a real dataset with NumPy, pandas and matplotlib, run an honest A/B test, and has every piece of linear algebra, calculus, probability and information theory that Phase 8 (classical ML) and Phase 9 (deep learning) consume, learned code-first and in the order those phases use it.

Every Topic below lists:
- **Learned when** — what the Learner must show, on top of the standard rule (Exercises pass without hints, Explain-back, later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during Explain-back and Spaced Reviews.
- **Sources** — the pages the Tutor teaches against; read on 2026-09-18.
- **Exercises** — folder names under this directory, in order.

Exercise folder layout: `exercise.md` (problem, examples, constraints, Hint Ladder, Explain-back questions), then `starter.py`/`test.py`/`reference.py`. Exercises are Python-only. `numpy`, `pandas`, `matplotlib`, `scikit-learn` and PyTorch CPU are all installed; each exercise says which of them it allows (a "pure Python" exercise allows none, and a test may still use NumPy or pandas to compute the expected values). DataFrame Topics use real pandas: the test builds small DataFrames from literal data, the function takes and returns DataFrames or Series, and the test compares with `pandas.testing` or tolerances. The matplotlib exercise builds a `Figure` under the `Agg` backend and never shows a window. Every exercise is deterministic and fast: a pure function or small class whose numerical answers the test compares with tolerances, anything random takes a seed or a `random.Random`/`numpy.random.Generator` argument, no file or network access, and every test finishes in a few seconds. The reference is only used by `scripts/verify-exercises.mjs` to prove the tests are correct; the Tutor never shows it.

---

## 1. NumPy arrays and vectorization

**Learned when:** the Learner replaces a Python loop over numbers with one array expression, predicts the shape and dtype of the result, and explains why the array version is faster.

**Teach:** `ndarray` as a contiguous block plus shape and dtype; creating arrays (`array`, `zeros`, `arange`, `linspace`, `random.default_rng(seed)`); shape, `ndim`, `reshape`, `-1`; indexing and slicing return views, not copies; boolean masks and fancy indexing; elementwise ops and ufuncs; reductions with `axis` (axis 0 collapses rows, leaving per-column results); `keepdims`; vectorization: one C loop instead of many Python steps; broadcasting as the rule that lets a row vector meet a matrix (formalized in Topic 3); float precision (`float32` vs `float64`) and integer overflow in fixed-width dtypes; `np.allclose` for comparing floats.

**Probe:** mutating a slice and being surprised the original changed; `axis=0` read as "along a row"; comparing float arrays with `==`; a Python `for` loop over array rows called "vectorized"; assuming integer arrays grow like Python ints instead of overflowing; `reshape` believed to move data rather than reinterpret it.

**Sources:** https://d2l.ai/ (ch 2 preliminaries), https://madewithml.com/, https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `01-01-column-stats` — per-column mean, standard deviation, min and max of a 2-D array with one reduction per statistic and no Python loops.
- `01-02-mask-and-replace` — replace every value more than k standard deviations from its column mean with that column's median, using boolean masks only.
- `01-03-pairwise-distances` — the full n×m matrix of Euclidean distances between two point sets with no Python loops, fast for 2000×2000 and equal to a loop version within tolerance.

## 2. Vectors, dot product, norms

**Learned when:** the Learner computes a dot product by hand, explains it as "how much one vector points along another", and picks cosine similarity or Euclidean distance for a given task with a reason.

**Teach:** a vector as a list of numbers and as an arrow; in ML a vector is usually one feature row; addition and scalar multiplication; dot product as sum of products and as |a||b|cos θ; L1 and L2 norms, unit vectors; Euclidean distance; cosine similarity ignores magnitude, distance does not; orthogonality means dot product zero; projection of a onto b; shape and dimension; the same operations in pure Python and as `np.dot`/`np.linalg.norm`.

**Probe:** dot product confused with elementwise multiplication; cosine similarity of 1 read as "identical vectors"; claiming distance and cosine always rank neighbors the same way; a norm of a difference read as a norm difference; the zero vector fed to cosine similarity without a guard.

**Sources:** https://mml-book.github.io/ (ch 2–3), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `02-01-dot-and-norms` — `dot`, `norm(v, p)` for p = 1 and 2, and `cosine_similarity`, all raising on length mismatch, in pure Python.
- `02-02-nearest-vector` — index of the nearest vector to a query by cosine and by Euclidean distance, with a test set where the two disagree.
- `02-03-project-onto` — the projection of a onto b and the leftover orthogonal component, with the test checking the two parts add back up and are orthogonal.

## 3. Matrices, matrix multiplication and broadcasting

**Learned when:** the Learner predicts the output shape of any matmul or broadcast, or says why it fails, and explains `Xw + b` as "one dot product per example, then a bias added by broadcasting".

**Teach:** matrix shape m×n; matmul rule (m×n)(n×p) → (m×p); row·column view and "many dot products at once"; matmul as a linear transformation of each row; transpose; identity; elementwise (Hadamard) product vs matmul; `A*B` vs `A@B` in NumPy; a batch of examples as matrix X with rows = examples; `Xw + b`; NumPy broadcasting rules: align shapes from the right, dimensions must be equal or 1; the bias vector reaching every row through broadcasting; silent bugs when a (n,) meets a (n,1); matmul is not commutative; cost of matmul is O(mnp).

**Probe:** `A*B` used for matmul; assuming `AB = BA`; a (3,) and (3,1) broadcast into (3,3) without noticing; reading `X @ w` with `w` a column vs a 1-D array; transposing a square matrix and thinking nothing changed; calling broadcasting "copying the data".

**Sources:** https://mml-book.github.io/ (ch 2), https://d2l.ai/ (ch 2 preliminaries), https://course.fast.ai/ (lesson 11, matrix multiplication)

**Exercises:**
- `03-01-matmul-lists` — matmul and transpose on lists of lists with a shape-mismatch error, checked against NumPy.
- `03-02-broadcast-shape` — NumPy's broadcasting rules on shape tuples: return the result shape or raise, covering leading-dimension padding and size-1 stretching.
- `03-03-affine-batch` — `XW + b` for a batch of rows both in pure Python and in NumPy, with the two agreeing and the shape of every intermediate asserted.

## 4. Linear systems, inverse, determinant

**Learned when:** the Learner solves a 3×3 system by elimination, explains what "XᵀX is singular" will mean for least squares, and says why code should call a solver instead of computing an inverse.

**Teach:** a system Ax = b as "find the weights that combine the columns of A into b"; Gaussian elimination with partial pivoting; back substitution; inverse exists iff det ≠ 0; determinant as signed volume scaling, computed from the elimination pivots; rank and linear dependence; a determinant near zero means ill-conditioned, not merely small numbers; why explicit inverses are numerically worse than `np.linalg.solve`; `np.linalg.solve`, `np.linalg.inv`, `np.linalg.matrix_rank`; O(n³) cost.

**Probe:** computing `inv(A) @ b` when `solve(A, b)` is available; "det is small so the matrix is nearly singular" without scaling in mind; elimination without pivoting dividing by a tiny pivot; a duplicated feature column not recognized as a rank drop; belief that every square system has exactly one solution.

**Sources:** https://mml-book.github.io/ (ch 2), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `04-01-determinant` — determinant of an n×n matrix via elimination, matching `np.linalg.det` within tolerance including sign.
- `04-02-solve-gaussian` — solve Ax = b with partial pivoting, raising on a singular system, matching `np.linalg.solve`.
- `04-03-matrix-rank` — rank via row echelon form with a tolerance, plus `is_singular`, correct on a matrix with a duplicated column and on floating-point near-dependence.

## 5. pandas DataFrames and loading data

**Learned when:** the Learner loads a CSV, JSON and Parquet file into a DataFrame, answers a question with a select–filter–groupby–aggregate chain, joins two tables, and explains what each step does row by row.

**Teach:** `Series` and `DataFrame` as labeled columns over NumPy arrays; index vs columns; `read_csv`, `read_json`, `read_parquet` and when each format is used (CSV: universal, untyped; JSON: nested, from APIs; Parquet: columnar, typed, compressed); dtype inference and its failures (numbers as strings, dates); `head`, `info`, `describe`, `value_counts`; selection with `[]`, `loc`, `iloc`, boolean filters; `groupby` then aggregate; `merge` (inner/left/outer) and one-to-many blow-ups; `sort_values`; missing values as `NaN`, `isna`, `fillna`, `dropna`; `apply` vs vectorized column ops; chained-assignment warnings and copies; writing back with `to_csv`/`to_parquet`; data sources beyond files: SQL queries into a DataFrame, API responses.

**Probe:** `df[df.col > 0]` read as mutating `df`; `loc` and `iloc` used interchangeably; a left join that multiplied rows blamed on pandas; `apply` with a Python function called vectorized; `NaN == NaN` expected to be true; choosing CSV for a 10 GB typed table; forgetting that `groupby` drops rows whose key is missing.

**Sources:** https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content, https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/data-analyst/content, https://madewithml.com/

**Exercises:**
- `05-01-load-csv-typed` — `load_typed_csv(text, date_columns)` reads CSV text with `pd.read_csv` and fixes dtype inference: strips `$` and thousands separators from numeric columns, parses date columns to `datetime64`, and turns empty, `NA` and `n/a` cells into `NaN`.
- `05-02-group-aggregate` — `revenue_by_region(orders)` as a filter–groupby–aggregate chain (paid orders only; count, revenue and mean order value per region, sorted by revenue) and `share_by_status(orders)` from normalized `value_counts`, with the test showing a `NaN` region is dropped by `groupby`.
- `05-03-join-records` — `enrich_orders(orders, customers, how)` with `merge` (inner or left on `customer_id`, one-to-many duplication and `NaN` fill checked) and `orders_per_customer(orders, customers)` counting zero for customers with no orders.

## 6. Visualization with matplotlib

**Learned when:** the Learner picks the right chart for a question (distribution, relationship, trend, comparison), builds it with the `Figure`/`Axes` API with labeled axes, and reads a histogram, scatter and box plot back into a claim about the data.

**Teach:** `fig, ax = plt.subplots()`; the Axes object owns the plot; `ax.plot`, `ax.scatter`, `ax.hist`, `ax.bar`, `ax.boxplot`, `ax.imshow` for heatmaps; labels, titles, legends; log scales for skewed data; chart choice: histogram for one distribution, scatter for two numeric columns, line for order or time, bar for categories, box plot for comparing groups; how a histogram's bin count changes the story; box plot parts (quartiles, IQR, whiskers at 1.5·IQR, outliers); correlation heatmaps; small multiples; loss curves as the DL diagnostic chart; saving with `savefig`; seaborn as a thin layer over matplotlib.

**Probe:** a line chart for unordered categories; a histogram with 3 bins used to claim "no outliers"; axis without units or label; the box plot's box read as the range; a truncated y-axis exaggerating a difference; treating a scatter with correlation as showing cause.

**Sources:** https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/data-analyst/content, https://developers.google.com/machine-learning/guides (Good Data Analysis)

**Exercises:**
- `06-01-histogram-counts` — bin counts and edges for a list of values in k equal-width bins, matching `np.histogram` including the closed last edge.
- `06-02-boxplot-summary` — quartiles, IQR, whisker ends and outliers for a sample exactly as a box plot computes them.
- `06-03-plot-learning-curves` — (matplotlib) build a `Figure` with train and validation loss lines, axis labels and a legend; the test reads the line data and labels back from the `Axes`.

## 7. EDA, data cleaning and data quality

**Learned when:** the Learner takes an unfamiliar table through a written EDA checklist, finds its missing values, duplicates, outliers and suspicious columns, and fixes them without leaking information from the test rows.

**Teach:** the EDA loop: question, look, summarize, plot, doubt; descriptive statistics (mean vs median, std, skewness, kurtosis) and which are robust; missing data: mechanism (missing at random or not), rates per column, imputation (median, mode, constant plus an indicator) fit on the training rows only; duplicates and near-duplicates; outliers by z-score or IQR and the decision to drop, cap or keep; inconsistent categories and units; constant and ID-like columns; class balance; train/test distribution shift; data traps: sampling bias, survivorship, Simpson's paradox, leakage columns that encode the label; keeping a data-quality report as an artifact.

**Probe:** imputing with the mean of the whole dataset before splitting; dropping every row with any missing value without checking how many go; an outlier removed because it is inconvenient; an ID column left in as a feature; a column correlated 0.99 with the label welcomed rather than suspected; skewed data summarized by its mean.

**Sources:** https://developers.google.com/machine-learning/guides (Good Data Analysis, Data Traps), https://madewithml.com/ (exploratory data analysis), https://fullstackdeeplearning.com/course/2022/ (lecture 4, data management)

**Exercises:**
- `07-01-describe-column` — `describe_column(s)` returns a `Series` of count, missing count, mean, median, std, skewness, min and max for a numeric `Series` containing `NaN`, matching NumPy on the non-missing values within tolerance.
- `07-02-imputer-and-outliers` — an `Imputer` class with `fit(train)`/`transform(df)` over DataFrames that fills `NaN` with the train medians and adds `<col>_missing` indicator columns without mutating its input, plus `iqr_outlier_mask(df, k)` returning a boolean DataFrame.
- `07-03-data-quality-report` — `quality_report(train, test, k)` over DataFrames: duplicate row count, missing rate per column as a `Series`, constant columns, ID-like columns and numeric columns whose test mean drifts more than k train standard deviations from the train mean.

## 8. Probability for ML

**Learned when:** the Learner interprets a model output of 0.8 as a probability, computes an expectation and variance from a distribution, applies Bayes' rule to a base-rate problem, and samples from a categorical distribution reproducibly.

**Teach:** random variable; discrete vs continuous; PMF vs PDF and why a density can exceed 1; Bernoulli, categorical, uniform, Gaussian; expectation as a probability-weighted average; variance and standard deviation; sample vs population variance (`ddof`); joint, marginal and conditional probability; independence; Bayes' rule and the base-rate fallacy; sampling with a seeded generator; law of large numbers as "frequencies converge"; a model's probability output vs a calibrated probability.

**Probe:** P(A|B) swapped with P(B|A); a PDF value read as a probability; "variance is the average deviation"; independence assumed because two things are unrelated in the story; a softmax output taken as calibrated; expecting a seeded sampler to give exact frequencies rather than approximate ones.

**Sources:** https://mml-book.github.io/ (ch 6), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `08-01-bayes-rule` — `bayes(prior, likelihood, evidence)` and a `posterior_positive_test(prevalence, sensitivity, specificity)` word problem in pure Python.
- `08-02-moments-and-pdfs` — `mean`, `variance(sample, ddof)`, `expectation(values, probs)`, `gaussian_pdf` and `bernoulli_pmf`, checked against NumPy and closed forms.
- `08-03-sample-categorical` — a seeded categorical sampler over a probability list, with empirical frequencies within tolerance of the probabilities after 10 000 draws and rejecting probabilities that do not sum to 1.

## 9. Inferential statistics and A/B testing

**Learned when:** the Learner runs an A/B test end to end (sample size, test statistic, p-value, confidence interval), states what the p-value does and does not mean, and explains why a correlation in observational data is not a cause.

**Teach:** population vs sample; sampling distribution and standard error; confidence interval for a mean and for a proportion; null and alternative hypothesis; test statistic, p-value, significance level, type I and II errors and power; z-test for two proportions (the A/B test), Welch's t-test idea; the normal CDF from `math.erfc`; sample-size planning from a minimum detectable effect; peeking and multiple comparisons; permutation tests and the bootstrap as compute-instead-of-formula methods; Pearson and Spearman correlation; correlation vs causation, confounders, randomization as the fix; practical vs statistical significance.

**Probe:** "p = 0.03 means a 97% chance B is better"; stopping the test as soon as p dips below 0.05; a 95% CI read as "95% of the data lies here"; correlation of 0.9 called a strong cause; running 20 metrics and reporting the one that hit significance; using a t-test on heavily skewed data with n = 5 without concern.

**Sources:** https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/data-analyst/content, https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/ai-data-scientist/content

**Exercises:**
- `09-01-correlation` — Pearson r and Spearman rank correlation with average ranks for ties, in pure Python, matching NumPy.
- `09-02-confidence-intervals` — normal-approximation confidence intervals for a mean and a proportion at a given z, and the sample size needed for a target margin of error.
- `09-03-ab-test` — two-proportion z-test returning the statistic and two-sided p-value via `math.erfc`, plus a seeded permutation test and bootstrap interval for a difference in means.

## 10. Derivatives and the chain rule

**Learned when:** the Learner differentiates `sigmoid(w*x + b)` with respect to w by hand, checks it with a central difference, and explains why numeric derivatives are for checking, not training.

**Teach:** derivative as slope and as best local linear approximation; derivatives of x^n, e^x, log x, sigmoid, tanh, relu; product rule; chain rule as "multiply the local derivatives along the path"; central difference `(f(x+h) − f(x−h)) / 2h` and how the error shrinks with h until float noise takes over; sigmoid' = σ(1−σ), tanh' = 1 − tanh²; relu's kink at 0 and the subgradient convention; why numeric differentiation is too slow and imprecise for millions of parameters.

**Probe:** chain rule terms added instead of multiplied; the forward difference used and the error blamed on floats; `h = 1e-12` "for more precision"; relu declared non-differentiable and therefore unusable; the derivative of a composition evaluated at the wrong inner point.

**Sources:** https://mml-book.github.io/ (ch 5), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `10-01-numeric-derivative` — central-difference `numeric_derivative(f, x, h)` tested against known derivatives, with the error shrinking as h shrinks from 1e-2 to 1e-5.
- `10-02-activation-derivatives` — sigmoid, tanh, relu and their derivatives, each checked against the numeric derivative at many points.
- `10-03-chain-rule-composed` — the derivative of `f_k(...f_1(x))` from a list of (function, derivative) pairs applied by the chain rule, checked numerically.

## 11. Partial derivatives, gradients and Jacobians

**Learned when:** the Learner derives ∇L for MSE with respect to w and b, matches it to a numeric gradient, and explains why a step against the gradient lowers the loss.

**Teach:** partial derivative holds the other inputs fixed; the gradient vector has the same shape as the parameters; the gradient is the direction of steepest ascent in parameter space; multivariable chain rule sums over paths, which is the `+=` in every autograd engine; Jacobian for vector-to-vector functions; the Hessian as curvature, named only; the analytic gradient of MSE `(2/n) Σ (ŷ−y)·x` and `(2/n) Σ (ŷ−y)`; gradient checking with relative error; numeric gradients cost one function pair per parameter.

**Probe:** the gradient placed in input space instead of parameter space; a branching variable's contributions overwritten instead of summed; the gradient's shape not matching the parameter's; a gradient check passed with absolute error on values of size 1e6; the Hessian believed necessary for training.

**Sources:** https://mml-book.github.io/ (ch 5), https://d2l.ai/ (ch 2, calculus and automatic differentiation)

**Exercises:**
- `11-01-numeric-gradient` — `numeric_gradient(f, params)` over a list of floats by central differences, tested on quadratics and on a function with interacting parameters.
- `11-02-mse-gradient` — the analytic gradient of MSE with respect to w and b for `y = wx + b`, matching the numeric gradient on several datasets.
- `11-03-jacobian-and-gradcheck` — a numeric Jacobian for f: Rⁿ → Rᵐ and `gradient_check(analytic, numeric)` returning the relative error, with a test that a deliberately wrong analytic gradient fails.

## 12. Optimization basics

**Learned when:** the Learner implements gradient descent on any differentiable function, reads a trajectory to say whether the learning rate is too high or too low, and explains convexity's role for linear and logistic regression.

**Teach:** objective, minimum, local vs global; convex functions have one basin (linear and logistic regression are convex, neural nets are not); step size / learning rate; the update `x -= lr * grad`; convergence and divergence, with `lr > 2/L` diverging on a quadratic with curvature L; oscillation at a borderline rate; stopping criteria (gradient norm, loss change, max steps); badly scaled problems and why feature scaling helps; backtracking line search as an adaptive step; saddle points and plateaus as the real high-dimensional problem, not local minima.

**Probe:** a loss that grows blamed on a bug rather than the learning rate; "bigger learning rate = faster"; stopping on a fixed step count with no convergence check; assuming GD finds the global minimum of any function; a local minimum called the main obstacle in deep learning.

**Sources:** https://mml-book.github.io/ (ch 7), https://d2l.ai/ (ch 12 optimization)

**Exercises:**
- `12-01-gradient-descent` — `gradient_descent(grad_f, x0, lr, steps)` returning the trajectory, converging on a quadratic and diverging when `lr > 2/L`.
- `12-02-minimize-1d` — minimize a 1-D function with a numeric gradient and a tolerance-based stop, returning the minimizer and the number of steps taken.
- `12-03-line-search-descent` — gradient descent with backtracking (Armijo) line search that converges on a badly scaled quadratic where a fixed learning rate either diverges or crawls.

## 13. Likelihood, entropy and cross-entropy

**Learned when:** the Learner explains why "minimize cross-entropy" equals "maximize likelihood", why logs are used, and writes a log-sum-exp that survives inputs of 1000.

**Teach:** likelihood of data under a model; the i.i.d. assumption turns a joint into a product; logs turn products into sums and avoid underflow; negative log-likelihood as the loss; maximum-likelihood estimation; MSE is the NLL of Gaussian noise, BCE is the NLL of Bernoulli outputs; entropy as expected surprise; cross-entropy and KL divergence, KL ≥ 0 and asymmetric; the log-sum-exp trick and `log_softmax`; `log(0)` and float overflow as real bugs, so clip or work in logits; accuracy is not differentiable, log-loss is.

**Probe:** cross-entropy assumed symmetric; `math.exp(1000)` inside a softmax; probabilities clipped at 0 producing `-inf` loss; the MLE of a Bernoulli believed to need gradient descent; entropy of a deterministic outcome given as 1; "we use logs because they are convenient" with no numerical reason.

**Sources:** https://d2l.ai/ (appendix, information theory), https://mml-book.github.io/ (ch 6, 8)

**Exercises:**
- `13-01-logsumexp` — `logsumexp(xs)` and `log_softmax(xs)` stable for `[1000, 1000]` and `[-1000, -1000]`, matching the naive formula on moderate values.
- `13-02-entropy-and-kl` — `entropy`, `cross_entropy` and `kl` over probability lists that treat `0·log 0` as 0, with tests that KL ≥ 0 and KL(p, p) = 0.
- `13-03-mle-and-nll` — `mle_bernoulli`, `mle_gaussian` (mean and variance) and `nll_bernoulli(ys, ps)`, with the test showing the NLL equals the BCE formula and the MLE minimizes it.

## 14. Eigenvectors and SVD, just enough for PCA

**Learned when:** the Learner explains PCA as "the top eigenvectors of the covariance matrix are the directions of most variance", finds the dominant eigenvector by power iteration, and reads what `np.linalg.svd` returns.

**Teach:** an eigenvector keeps its direction under A, scaled by its eigenvalue; covariance matrix from centered data; symmetric matrices have real eigenvalues and orthogonal eigenvectors; power iteration and why it converges to the largest eigenvalue; deflation to find the next one; SVD X = UΣVᵀ as the general factorization; singular values squared are the eigenvalues of XᵀX; low-rank approximation keeps the top-k singular values and the dropped energy is the sum of the squared rest; eigenvectors are defined only up to sign and scale; you read SVD results, you do not hand-compute them.

**Probe:** a test that fails because an eigenvector came back with the opposite sign; covariance computed on uncentered data; the largest singular value confused with the largest eigenvalue of X itself; expecting power iteration to find all eigenvectors at once; `np.linalg.svd` returning V rather than Vᵀ.

**Sources:** https://mml-book.github.io/ (ch 4, 10), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `14-01-covariance-matrix` — the covariance matrix of a list of rows with `ddof`, in pure Python, matching `np.cov`.
- `14-02-power-iteration` — the dominant eigenpair of a symmetric matrix by power iteration, compared to NumPy up to sign, plus one deflation step for the second pair.
- `14-03-low-rank-approximation` — rank-k reconstruction with `np.linalg.svd`, with the Frobenius error equal to the dropped singular values' energy and `explained_variance(X, k)` as a fraction.
