# Phase 8 — Classical machine learning

About 105 hours over about 8 weeks, 20 Topics. For a Learner who has finished Phase 7 (NumPy, pandas, EDA, the math). At the end the Learner can take a raw table to an honestly evaluated model: frame the task, beat a baseline, train linear, logistic, tree and ensemble models written from scratch, choose and tune them with cross-validation, cluster and reduce data, flag anomalies, recommend items, explain a tabular model, check it for unfairness, and say from an error analysis what to fix next.

Every Topic below lists:
- **Learned when** — what the Learner must show, on top of the standard rule (Exercises pass without hints, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Sources** — the pages the Tutor teaches against; read on 2026-09-18.
- **Exercises** — folder names under this directory, in order.

Exercise folder layout: `exercise.md` (problem, examples, constraints, Hint Ladder, and the questions the Breakdown answers), then `starter.py`/`test.py`/`reference.py`. Exercises are Python-only. They may use `numpy` (installed) and PyTorch CPU (installed); `matplotlib` only where an exercise is marked (matplotlib). scikit-learn is installed, but no exercise allows it in the solution: every model here is written by the Learner (a test may use it to compute expected values). Every exercise is a pure function or small class whose numerical answers the test compares with tolerances; anything random takes a seed or a `random.Random`/`numpy.random.Generator` argument, and every test finishes in a few seconds. The reference is only used by `scripts/verify-exercises.mjs` to prove the tests are correct; it is shown in the Breakdown once the Learner's own solution passes.

---

## 1. Framing a problem, baselines, and when not to use ML

**Learned when:** for a given product problem the Learner names the features, label, task type, loss, metric and trivial baseline, and says whether a rule would do instead of a model.

**Teach:** supervised vs unsupervised vs self-supervised vs reinforcement learning; features and label; a model as a parameterized function; training as minimizing a loss on data; inference; regression vs classification vs clustering vs ranking; the trivial baseline (mean, majority class, last value) and a heuristic baseline (a hand-written rule); relative error reduction over the baseline as the honest gain; when not to use ML: a rule already works, no labels, no tolerance for errors, the label is not measurable, the data will not exist at inference time; "ML is only as good as the features and loss allow"; ML project lifecycle as loop, not pipeline.

**Probe:** "beats random" accepted as success; a 92% accuracy celebrated before the majority-class rate is known; features chosen that will not exist at prediction time; a proxy label mistaken for the real goal; reaching for a model where a threshold rule is enough; unsupervised learning described as "no data".

**Sources:** https://developers.google.com/machine-learning/crash-course, https://developers.google.com/machine-learning/guides (Rules of ML), https://fullstackdeeplearning.com/course/2022/ (lecture 1, when to use ML)

**Exercises:**
- `01-01-baseline-regression` — predict-the-mean baseline and its MSE on a validation set, in pure Python.
- `01-02-baseline-classifier` — majority-class baseline and a seeded class-frequency random baseline, each with its accuracy.
- `01-03-heuristic-baseline` — a keyword-rule text classifier with its accuracy, and `improvement_over_baseline(model_score, baseline_score)` as relative error reduction, negative when the model is worse.

## 2. Linear regression and MSE, closed form

**Learned when:** the Learner fits `y = wx + b` by least squares, derives the normal equations from "gradient equals zero", and explains residuals, MSE and why polynomial regression is still linear.

**Teach:** hypothesis `ŷ = Xw + b`; residual; MSE, RMSE, MAE and their outlier sensitivity; R² and what a negative R² means; least squares as minimizing squared residuals; the normal equations `(XᵀX)w = Xᵀy` solved with Phase 7's solver, never with an explicit inverse; the bias trick (a column of ones); polynomial features are linear in the parameters; a singular XᵀX from duplicated or too many features; the closed form as the reference that gradient descent must match.

**Probe:** "linear" read as linear in the inputs; R² near 1 taken as causation; MSE chosen for a target with wild outliers without thought; the bias term forgotten; fitting a degree-9 polynomial to 10 points and calling it a good fit.

**Sources:** https://cs229.stanford.edu/ (lecture 1), https://d2l.ai/ (ch 3, linear regression), https://developers.google.com/machine-learning/crash-course (Linear Regression)

**Exercises:**
- `02-01-fit-line` — `fit_line(xs, ys)` returning (w, b) by least squares, matching `np.polyfit` within tolerance.
- `02-02-regression-metrics` — `mse`, `mae`, `rmse` and `r2`, including R² for a constant prediction and for one worse than the mean.
- `02-03-polynomial-regression` — `polynomial_features(xs, degree)` and a fit via the normal equations and Phase 7's Gaussian solver that recovers a cubic's coefficients exactly.

## 3. Gradient descent for linear regression

**Learned when:** the Learner trains linear regression with batch, stochastic and minibatch gradient descent, matches the closed form within tolerance, and diagnoses a bad learning rate or unscaled features from the loss curve.

**Teach:** the loss surface of MSE is a bowl; gradient of MSE with respect to w and b; the update `w -= lr * grad`; epoch; batch vs stochastic vs minibatch and the noise each brings; shuffling every epoch; learning-rate effects; a loss going to NaN means the rate is too high or the features are unscaled; convergence check; parameters vs hyperparameters; the vectorized version with NumPy as one matmul per step.

**Probe:** an SGD loss curve's noise treated as a bug; training order never shuffled; the closed form and GD expected to differ meaningfully; a learning rate copied from a tutorial applied to unscaled features; minibatches that skip or repeat rows.

**Sources:** https://cs229.stanford.edu/ (lectures 2 and 5), https://developers.google.com/machine-learning/crash-course (Linear Regression: gradient descent, hyperparameters), https://d2l.ai/ (ch 3 and 12)

**Exercises:**
- `03-01-gd-linreg-1d` — `gd_linreg_1d(xs, ys, lr, epochs)` returning (w, b, loss_history), converging to the closed form within tolerance with a non-increasing loss.
- `03-02-minibatches` — `minibatches(n, batch_size, rng)` yielding shuffled index batches that cover every index exactly once, including a short last batch.
- `03-03-sgd-linreg-vectorized` — multi-feature minibatch SGD in NumPy with standardized features that reaches the normal-equation solution within tolerance in few epochs.

## 4. Features: scaling, encoding and feature engineering

**Learned when:** the Learner prepares a mixed numeric and categorical table for a model with every statistic fitted on the training rows only, and says which models need scaling and which do not.

**Teach:** standardization (z-score) and min-max scaling; log transform for skewed positives; one-hot encoding with an unknown bucket; label encoding invents an order for nominal categories; hashing for huge vocabularies; feature crosses; binning/bucketizing; missing-value handling as a feature step; the fit/transform split: fit on train, transform everything; scaling matters for gradient descent, kNN, PCA and regularization but not for trees; outlier clipping; feature selection by correlation and by importance, both leak if done on the full data.

**Probe:** the scaler fit on the whole dataset before splitting; nominal categories mapped to 0, 1, 2 and fed to linear regression; an unseen category crashing inference; "trees need scaling too"; a one-hot column for every category of a 10 000-value ID; test rows used to pick features.

**Sources:** https://developers.google.com/machine-learning/crash-course (Working with Numerical Data, Working with Categorical Data), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `04-01-standard-scaler` — a `StandardScaler` class with `fit(train)`/`transform(rows)`; the test verifies the transform uses train statistics and handles a zero-variance column.
- `04-02-one-hot` — `one_hot(values, vocabulary)` with an unknown-category bucket and a stable column order, plus `bucketize(x, boundaries)`.
- `04-03-preprocessor` — a `Preprocessor` class combining log transform, bucketizing, scaling and one-hot per column spec, with `fit` on train and `transform` that never recomputes statistics.

## 5. Train, validation, test, cross-validation and leakage

**Learned when:** the Learner explains what each split is for, implements k-fold and stratified splits correctly, and spots leakage in a described pipeline.

**Teach:** generalization; holdout; validation for choosing hyperparameters, test for the one final estimate; k-fold cross-validation and its cost; leave-one-out; stratification for imbalanced classes; time-series splits never shuffle and only train on the past; grouped splits when rows share an entity; data leakage: duplicates across splits, target leakage columns, preprocessing fit on everything, tuning on the test set; the test score is reported once.

**Probe:** the test set consulted during development and still called "test"; random splits on time-ordered data; near-duplicate rows on both sides of the split; k-fold folds that overlap or miss an index; stratification skipped with 2% positives.

**Sources:** https://cs229.stanford.edu/ (lecture 3), https://developers.google.com/machine-learning/crash-course (Datasets, Generalization, and Overfitting), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `05-01-train-val-test-split` — `train_val_test_split(n, fracs, seed)` returning disjoint index lists that together cover every index, deterministic for a seed.
- `05-02-kfold-indices` — `kfold_indices(n, k)` where every index lands in exactly one validation fold and fold sizes differ by at most one.
- `05-03-stratified-and-time-splits` — a stratified split preserving each class's ratio within ±1 row, and expanding-window time-series splits whose validation block always follows its training block.

## 6. Overfitting, bias–variance and regularization

**Learned when:** the Learner reads train and validation curves to diagnose underfitting or overfitting, applies L2 or L1 with a chosen λ, and explains why L1 gives exact zeros.

**Teach:** capacity; underfitting vs overfitting; the bias–variance trade-off and the classic U-curve; learning curves against training-set size; L2 penalty (weight decay) shrinks weights; L1 penalty produces sparsity through soft-thresholding; elastic net; λ is a hyperparameter chosen on validation; the bias term is not regularized; early stopping as regularization; more data as a regularizer; ridge closed form `(XᵀX + λI)w = Xᵀy`; double descent in overparameterized nets, mentioned only.

**Probe:** low training loss taken as success; the bias term penalized; L2 expected to zero out weights; λ tuned on the test set; regularization added to a model that is underfitting; early stopping done without a patience window.

**Sources:** https://cs229.stanford.edu/ (lectures 2–3), https://d2l.ai/ (ch 3, weight decay and generalization), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `06-01-ridge-closed-form` — `ridge_closed_form(X, y, lam)` with an unpenalized bias, where weights shrink monotonically as λ grows and λ = 0 matches least squares.
- `06-02-l2-and-soft-threshold` — `gd_step_with_l2(w, grad, lr, lam)` and `soft_threshold(w, t)` as the L1 step, with a test that L1 yields exact zeros and L2 does not.
- `06-03-early-stopping-diagnosis` — `early_stopping_epoch(val_losses, patience)` and `diagnose(train_losses, val_losses)` returning underfit, overfit or ok from the final losses and their gap.

## 7. Logistic regression and binary cross-entropy

**Learned when:** the Learner trains a binary classifier with gradient descent, explains why the loss is BCE and not MSE, and writes sigmoid and BCE that do not overflow.

**Teach:** logit; sigmoid maps a logit to a probability; the decision boundary is linear in the features; BCE / log-loss as the Bernoulli negative log-likelihood from Phase 7; gradient `(p − y)·x`; the 0.5 threshold is a choice; MSE with sigmoid is non-convex and learns slowly; a numerically stable sigmoid using the sign of z; BCE from logits via `max(z, 0) − z·y + log(1 + exp(−|z|))`; class weights for imbalance.

**Probe:** logistic regression called regression; `math.exp(1000)` overflow met with a try/except; `log(p)` with p exactly 0; the 0.5 threshold treated as fixed; the boundary believed to bend because the sigmoid curves; MSE used "because it is simpler".

**Sources:** https://cs229.stanford.edu/ (lecture 4), https://developers.google.com/machine-learning/crash-course (Logistic Regression), https://d2l.ai/ (ch 4)

**Exercises:**
- `07-01-stable-sigmoid` — `stable_sigmoid(z)` with no overflow at ±1000, matching `1/(1+e^-z)` on moderate values, scalar and NumPy versions.
- `07-02-bce-with-logits` — `bce_with_logits(z, y)` stable for extreme logits, equal to the naive BCE on moderate values, with its gradient checked numerically.
- `07-03-train-logreg` — `train_logreg(X, y, lr, epochs)` reaching over 95% accuracy on a linearly separable toy set with a non-increasing loss.

## 8. Classification metrics

**Learned when:** given a use case the Learner picks the metric and threshold, computes it from a confusion matrix, and explains what AUC measures and does not.

**Teach:** confusion matrix; accuracy, precision, recall, F1, specificity; class imbalance makes accuracy worthless; precision and recall trade off through the threshold; ROC curve and AUC as the probability a random positive outranks a random negative, threshold-free; PR curve for rare positives; the rank (Mann–Whitney) formulation of AUC with ties; choosing a threshold on validation for the business metric; macro vs micro averaging for multiclass; calibration as "0.8 means 80%".

**Probe:** 99% accuracy on 1% positives celebrated; AUC believed to fix the threshold; precision and recall traded by changing the model rather than the threshold; F1 quoted with no positive-class definition; the ROC curve read on a heavily imbalanced set where PR would tell the truth.

**Sources:** https://developers.google.com/machine-learning/crash-course (Classification), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `08-01-confusion-and-prf` — `confusion_matrix(y_true, y_pred)` and `precision_recall_f1`, defined for the no-positive-predictions case, plus macro averaging for multiclass.
- `08-02-roc-auc` — `roc_auc(y_true, scores)` via the rank formulation with tie handling, matching a curve-integration version and giving 0.5 for random scores.
- `08-03-best-threshold` — `pr_curve(y_true, scores)` points and `best_threshold(y_true, scores, metric)` returning the threshold that maximizes F1 or a given precision floor.

## 9. Multiclass: softmax regression and categorical cross-entropy

**Learned when:** the Learner implements stable softmax and cross-entropy from logits, derives the gradient `p − onehot`, and trains a multiclass linear classifier.

**Teach:** a logit per class; softmax; subtracting the max for stability; categorical cross-entropy via log-sum-exp from Phase 7; the gradient with respect to logits is `p − y`; argmax prediction; top-k accuracy; temperature: softmax is shift-invariant but not scale-invariant; one-vs-rest as the alternative; never apply softmax before a loss that expects logits (the PyTorch `CrossEntropyLoss` double-softmax bug).

**Probe:** softmax on `[1000, 1001]` overflowing; softmax applied twice; the CE gradient believed to need the Jacobian of softmax spelled out; argmax over probabilities and over logits expected to differ; a temperature of 0 attempted.

**Sources:** https://d2l.ai/ (ch 4, softmax regression), https://cs231n.stanford.edu/schedule.html (lecture 2, linear classifiers)

**Exercises:**
- `09-01-stable-softmax` — `softmax(logits)` stable for `[1000, 1001]`, summing to 1, with `top_k_accuracy(logits_rows, targets, k)`.
- `09-02-ce-from-logits` — `cross_entropy_from_logits(logits, target_idx)` via log-sum-exp, equal to `-log(softmax[target])` on moderate values and finite on extreme ones.
- `09-03-softmax-regression` — a softmax regression trainer whose gradient `p − onehot` is checked numerically and which reaches over 90% on a three-class toy set.

## 10. k-nearest neighbors

**Learned when:** the Learner implements kNN classification and regression with deterministic tie-breaking, picks k by cross-validation, and explains why scaling and dimensionality matter.

**Teach:** instance-based, non-parametric learning; distance metrics; k as the bias–variance knob; majority vote and tie-breaking rules; distance-weighted voting; kNN regression as the neighbors' mean; O(n·d) query cost; the training cost is deferred, not absent; the curse of dimensionality: distances concentrate in high dimensions; unscaled features let one column dominate; choosing k with Phase 8's k-fold.

**Probe:** k = 1 with zero training error taken as perfection; an even k with no tie rule; "kNN has no training so it is fast"; distances computed on unscaled income and age; expecting kNN to work on 10 000-dimensional sparse text.

**Sources:** https://cs229.stanford.edu/ (lecture 6), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `10-01-knn-classify` — `knn_predict(train_X, train_y, x, k)` with majority vote and deterministic tie-breaking by nearest neighbor then smallest label.
- `10-02-knn-regress` — `knn_regress(train_X, train_y, x, k, weighted)` with an optional inverse-distance weighting and a guard for a zero distance.
- `10-03-choose-k` — `choose_k(X, y, ks, folds)` returning the k with the best cross-validated accuracy using the Topic 5 folds, ties going to the smaller k.

## 11. Decision trees

**Learned when:** the Learner builds a tree by greedy splits on Gini or entropy, predicts with it, and explains why an unlimited tree overfits and cannot extrapolate.

**Teach:** recursive partitioning; impurity (Gini, entropy) and information gain; candidate thresholds at midpoints between sorted values; stopping criteria (max depth, min samples, pure node); leaf prediction by majority or mean; regression trees by variance reduction; no scaling needed; interpretability of a shallow tree; greedy splits are not globally optimal; a deep tree has high variance; trees predict constants outside the training range.

**Probe:** thresholds tried only at data values, missing the midpoint; the gain computed without weighting children by size; a tree grown until every leaf is pure and called done; a tree expected to extrapolate a trend; categorical features one-hot encoded and believed necessary for trees.

**Sources:** https://cs229.stanford.edu/ (lecture 6), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `11-01-gini-entropy` — `gini(labels)` and `entropy(labels)` in pure Python, with pure and uniform label sets as edge cases.
- `11-02-best-split` — `best_split(X, y)` returning (feature, threshold, gain) using size-weighted impurity and midpoint thresholds.
- `11-03-decision-tree` — `build_tree(X, y, max_depth, min_samples)` as nested dicts and `predict_tree`, fitting a toy set perfectly at full depth and underfitting at depth 1.

## 12. Ensembles: bagging, random forests and gradient boosting

**Learned when:** the Learner explains why averaging reduces variance and boosting reduces bias, implements both on the Topic 11 tree, and names GBDT libraries as the tabular default.

**Teach:** bootstrap sampling; bagging as averaging models trained on resamples; out-of-bag rows as a free validation set; random forests add a random feature subset per split to decorrelate trees; more trees in a forest do not overfit; boosting fits each new model to the residuals of the ensemble so far; learning rate / shrinkage and number of rounds; boosting can overfit; XGBoost and LightGBM as the tabular default, usually the baseline deep learning has to beat; impurity-based feature importance and its bias toward high-cardinality features.

**Probe:** "deep learning beats everything on tables"; a random forest tuned by reducing trees to stop overfitting; boosting run for 5 000 rounds with no validation; bootstrap samples taken without replacement; feature importance from a forest read as causal.

**Sources:** https://cs229.stanford.edu/ (lecture 6), https://course.fast.ai/ (lesson 6, random forests), https://developers.google.com/machine-learning/advanced-courses (Decision Forests)

**Exercises:**
- `12-01-bootstrap-and-bagging` — `bootstrap_sample(n, rng)` with its out-of-bag indices and `bagged_predict(models, x)` by majority vote or mean.
- `12-02-random-forest` — a seeded `RandomForest` class over the Topic 11 tree with per-split feature subsets that beats a single full-depth tree on a noisy held-out toy set.
- `12-03-gradient-boost-stumps` — `gradient_boost_stumps(xs, ys, n_rounds, lr)` for 1-D regression with depth-1 stumps on residuals, where the training loss decreases every round.

## 13. Interpretability for tabular models

**Learned when:** the Learner explains a trained tabular model's predictions with permutation importance, partial dependence and Shapley values, and says what each can and cannot claim.

**Teach:** global vs local explanations; permutation importance: shuffle one column, measure the metric drop, repeat with a seed; impurity importance vs permutation importance and correlated-feature pitfalls; partial dependence: average prediction as one feature sweeps a grid; Shapley values as the fair split of `f(x) − E[f]` across features over all coalitions, computed exactly for few features by enumeration and approximated by SHAP in practice; the efficiency property (values sum to the difference); local explanations do not imply causation; explanations for stakeholders and for debugging.

**Probe:** importance read as causal effect; permutation importance run on the training set; a partial-dependence curve trusted where the feature has no data; Shapley values believed to require retraining the model; SHAP treated as a model rather than an explanation method.

**Sources:** https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content, https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/mlops/content

**Exercises:**
- `13-01-permutation-importance` — `permutation_importance(predict, X, y, metric, rng, repeats)` returning the mean metric drop per feature, deterministic for a seed.
- `13-02-partial-dependence` — `partial_dependence(predict, X, feature, grid)` returning the averaged prediction per grid value.
- `13-03-shapley-values` — exact Shapley values for a model with at most four features by enumerating coalitions against a background row, with the test checking they sum to `f(x) − f(background)`.

## 14. Clustering: k-means

**Learned when:** the Learner implements Lloyd's algorithm with k-means++ initialization, shows inertia never increases, and explains init sensitivity, the spherical assumption and how to pick k.

**Teach:** unsupervised: no labels; centroid; assignment and update steps; inertia (within-cluster sum of squares) is non-increasing; convergence to a local optimum; k-means++ initialization spreads the seeds; the elbow method and silhouette as ways to pick k; the spherical-cluster assumption and where it fails (rings, elongated clusters); scaled features required; the result depends on the seed; GMM as the soft version, mentioned only.

**Probe:** k-means expected to find the global optimum; clusters compared to labels as if clustering were classification; unscaled features; an empty cluster left unhandled; the elbow "found" on a curve with no elbow.

**Sources:** https://cs229.stanford.edu/ (lecture 9), https://course.fast.ai/ (lesson 12, clustering), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `14-01-assign-and-update` — `assign(points, centroids)` returning the nearest centroid index per point and `update(points, labels, k)` returning new centroids, with an empty cluster keeping its old centroid.
- `14-02-kmeans` — `kmeans(points, k, seed, iters)` returning centroids, labels and the inertia history, which never increases and recovers three well-separated blobs.
- `14-03-kmeans-pp-and-elbow` — `kmeans_pp_init(points, k, rng)` and `inertia_curve(points, ks, seed)` for the elbow plot, with k-means++ beating random init on a seeded hard case.

## 15. PCA and dimensionality reduction

**Learned when:** the Learner projects data onto its top-k principal components, reports the explained variance, reconstructs it, and explains why PCA is unsupervised and needs centered data.

**Teach:** centering (and usually scaling); covariance matrix; principal components are the eigenvectors of the covariance, sorted by eigenvalue; explained variance ratio; projection and reconstruction; the reconstruction error equals the dropped variance; PCA via SVD of the centered data; using PCA before kNN or for visualization; components are directions of variance, not "features that matter for the label"; t-SNE and UMAP for plots only, with distances between clusters not meaningful.

**Probe:** PCA run on uncentered data; the number of components chosen without looking at explained variance; PCA applied and then the components interpreted as labels; t-SNE cluster distances read as real; a sign flip in a component treated as a bug.

**Sources:** https://cs229.stanford.edu/ (lecture 11), https://mml-book.github.io/ (ch 10), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content

**Exercises:**
- `15-01-pca-2d-power-iteration` — `pca_2d(points)` via Phase 7's power iteration plus deflation, returning two components that match NumPy's up to sign.
- `15-02-explained-variance` — `explained_variance_ratio(X, k)` from the SVD of centered data, summing to 1 at full rank.
- `15-03-project-reconstruct` — `project(X, k)` and `reconstruct(Z, components, mean)` with a round-trip error equal to the dropped variance and zero at full rank.

## 16. Anomaly detection

**Learned when:** the Learner scores anomalies by z-score, IQR, a fitted Gaussian density and PCA reconstruction error, picks a threshold on a small labeled validation set, and explains why anomaly detection is not classification.

**Teach:** anomalies are rare, varied and often unlabeled, so a classifier is not an option; univariate rules: z-score, IQR; a per-feature Gaussian density fitted on normal data, with a low density meaning anomalous; choosing ε on a labeled validation set by F1, since accuracy is useless; multivariate anomalies that no single feature shows; PCA reconstruction error as a score; distance to the k-th nearest neighbor as a score; isolation forests, named only; precision and recall at the chosen threshold; drift: yesterday's normal is today's anomaly.

**Probe:** training the Gaussian on data that includes the anomalies; a threshold picked without any labeled example; the Gaussian applied to heavily skewed features without a log transform; an anomaly detector evaluated by accuracy; "we have 30 labeled fraud cases so let us train a classifier".

**Sources:** https://www.deeplearning.ai/courses/machine-learning-specialization/ (course 3, anomaly detection), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/ai-engineer/content

**Exercises:**
- `16-01-zscore-iqr-outliers` — `zscore_flags(xs, k)` and `iqr_flags(xs, factor)` returning boolean flags per value, matching hand-computed cases.
- `16-02-gaussian-anomaly` — a `GaussianAnomalyDetector` class fitted on normal rows with `score(rows)` as the log density and `choose_epsilon(scores, labels)` maximizing F1 on a validation set.
- `16-03-reconstruction-anomaly` — PCA reconstruction-error scores that rank planted multivariate anomalies at the top when no single feature is out of range.

## 17. Recommender systems basics

**Learned when:** the Learner builds collaborative filtering by user similarity and by matrix factorization, a content-based recommender, and explains sparsity, cold start and the feedback-loop risk.

**Teach:** the user–item ratings matrix and its sparsity; explicit vs implicit feedback; user-based collaborative filtering: similar users' ratings weighted by cosine similarity; item-based as the transpose; matrix factorization: user and item embeddings whose dot product predicts a rating, trained by gradient descent with L2 on the observed cells only; the connection to Phase 7's low-rank approximation; content-based: item feature vectors and a user profile from what they liked; cold start for new users and items and fallbacks (popularity, content); evaluation on held-out ratings (RMSE) and on ranking (precision@k); popularity bias and feedback loops; two-tower embedding retrieval as the modern version, mentioned as the Phase 9 handoff.

**Probe:** missing ratings treated as zeros; the factorization loss computed over unobserved cells; a similarity computed from one shared item trusted; a new user handled by crashing; RMSE on ratings taken as proof the top-10 list is good; recommending what is already popular and calling the model accurate.

**Sources:** https://developers.google.com/machine-learning/advanced-courses (Recommendation Systems), https://course.fast.ai/ (lesson 7, collaborative filtering), https://www.deeplearning.ai/courses/machine-learning-specialization/ (course 3, recommender systems)

**Exercises:**
- `17-01-user-based-cf` — `predict_rating(ratings, user, item, k)` from the k most cosine-similar users who rated the item, over a dict-of-dicts sparse matrix, with a fallback to the user's mean.
- `17-02-content-based` — `user_profile(item_features, liked)` and `recommend(profile, item_features, n, exclude)` ranking unseen items by cosine similarity with a stable tie order.
- `17-03-matrix-factorization` — a seeded `MatrixFactorization` class trained by gradient descent with L2 on observed cells only, reaching a held-out RMSE below a threshold on a planted low-rank ratings matrix.

## 18. Responsible AI: fairness, bias and privacy

**Learned when:** the Learner audits a classifier per group with fairness metrics, names where bias entered (data, label, features, feedback), and applies a privacy check before sharing a dataset.

**Teach:** where bias enters: historical data, sampling, label noise, proxy features (zip code for race), feedback loops; per-group evaluation as the first step; fairness metrics: demographic parity (selection rates), equalized odds (TPR and FPR per group), the four-fifths disparate-impact rule; the metrics conflict, so a choice must be made and written down; removing the protected column does not remove the proxies; privacy: PII, direct and quasi-identifiers, k-anonymity by generalization, re-identification from joins; differential privacy, named only; data ethics: consent, purpose, the cost of a false positive per person; model cards and documenting limits.

**Probe:** "we dropped gender so the model is fair"; equal accuracy across groups taken as fairness while error types differ; a fairness metric picked because it passed; a dataset called anonymous because names were removed; fairness treated as a final check rather than a design input.

**Sources:** https://developers.google.com/machine-learning/crash-course (Fairness), https://developers.google.com/machine-learning/guides (Introduction to Responsible AI), https://course.fast.ai/ (lesson 5, data ethics)

**Exercises:**
- `18-01-group-metrics` — `group_metrics(y_true, y_pred, groups)` returning selection rate, TPR, FPR and accuracy per group.
- `18-02-fairness-metrics` — demographic parity difference, equalized odds difference and the disparate-impact ratio from the group metrics, with a `passes_four_fifths` check.
- `18-03-k-anonymity` — `k_anonymity(records, quasi_ids)` returning the smallest equivalence-class size, and `generalize(records, quasi_ids, rules)` that bins and masks columns until a target k is reached.

## 19. Error analysis and project strategy

**Learned when:** the Learner looks at a model's worst errors by slice, compares human, training, train-dev and validation error to name the dominant problem, and decides what to do next: more data, a bigger model, better features or a different split.

**Teach:** error analysis: sample the errors, categorize them by hand, count the categories, fix the biggest; slice metrics by feature values and by data source; human-level error as a proxy for the floor; avoidable bias (train error above the floor) vs variance (validation above train) vs data mismatch (a train-dev set drawn from the training distribution separates the two) vs validation overfitting (test above validation); the learning curve against training-set size says whether more data will help; a single-number metric plus satisficing constraints (latency, size); optimize one thing at a time; when the label is wrong more often than the model, fix the labels.

**Probe:** more data collected for a model with high bias; the hardest error category chased first instead of the largest; a validation set from a different distribution than production; "the model is 90% accurate" with no slice below 60% noticed; hyperparameters swept before the labels were checked.

**Sources:** https://www.deeplearning.ai/courses/deep-learning-specialization/ (course 3, structuring ML projects), https://fullstackdeeplearning.com/course/2022/ (lecture 1 and troubleshooting), https://developers.google.com/machine-learning/guides (Rules of ML)

**Exercises:**
- `19-01-slice-metrics` — `slice_metrics(y_true, y_pred, feature_values, metric)` returning per-slice scores and support sorted worst first, and `worst_errors(y_true, scores, n)` as the most confident mistakes.
- `19-02-bias-variance-mismatch` — `diagnose(human, train, train_dev, dev, test)` naming the dominant gap: avoidable bias, variance, data mismatch or dev overfitting, with ties broken in that order.
- `19-03-learning-curve` — `learning_curve(fit, predict, X, y, sizes, folds)` returning train and validation error per training size, and `more_data_helps(curve)` from whether the gap is still closing.

## 20. The practical workflow: a scikit-learn-style capstone

**Learned when:** the Learner takes a CSV to a validated model with a leakage-proof pipeline, cross-validation, a baseline, a tuned model and one honest test score, and can name the scikit-learn objects that do each step.

**Teach:** the workflow: load and inspect (Phase 7), split, baseline, pipeline (preprocessing fitted inside each fold), cross-validation, a tuning search on validation, one test score, save the model, report uncertainty; `Pipeline`, `ColumnTransformer`, `cross_val_score`, `GridSearchCV`, `RandomizedSearchCV` as the scikit-learn names for what the Learner built; grid search as a Cartesian product, random search as sampling, log-uniform ranges for learning rates and λ; more search overfits validation; nested CV, named only; reproducibility with seeds and versioned data; the write-up: what was tried, what worked, what the score means; the handoff to Phase 9: the same workflow with a neural network as the model.

**Probe:** the scaler fitted once outside the folds; a search run over 2 000 configurations and the best validation score reported as the expected test score; the test set scored twice; a learning rate grid of 0.1, 0.2, 0.3; the model saved without its preprocessing; a result that cannot be reproduced from the seed.

**Sources:** https://developers.google.com/machine-learning/crash-course (Production ML Systems), https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/machine-learning/content, https://madewithml.com/

**Exercises:**
- `20-01-grid-search-space` — `grid(space)` returning the Cartesian product of a parameter space as dicts in a stable order.
- `20-02-random-search` — `random_search(space, n, rng)` sampling configurations from lists, uniform and log-uniform ranges, deterministic for a seed.
- `20-03-pipeline-cv` — a `Pipeline` class chaining fit/transform steps and a model with `cross_val_score(pipeline, X, y, folds, metric)` that fits preprocessing inside each fold; the test shows a leaky pre-fitted scaler gives a different score.
