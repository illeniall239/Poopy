import unittest

import numpy as np

from solution import Pipeline, cross_val_score


class StandardScaler:
    def fit(self, X):
        self.mean_ = X.mean(axis=0)
        self.std_ = X.std(axis=0)
        self.std_[self.std_ == 0] = 1.0
        return self

    def transform(self, X):
        return (X - self.mean_) / self.std_


class FrozenScaler(StandardScaler):
    """A scaler fitted once on ALL rows, whose fit() then does nothing: the leak."""

    def __init__(self, X_all):
        StandardScaler.fit(self, X_all)

    def fit(self, X):
        return self


class KNNRegressor:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_, self.y_ = X, y
        return self

    def predict(self, X):
        d = ((X[:, None, :] - self.X_[None, :, :]) ** 2).sum(axis=2)
        nearest = np.argsort(d, axis=1, kind="stable")[:, : self.k]
        return self.y_[nearest].mean(axis=1)


class AddOne:
    def fit(self, X):
        return self

    def transform(self, X):
        return X + 1.0


class Spy:
    """Records what each call receives, and passes X through unchanged."""

    def __init__(self):
        self.fit_rows = []
        self.transform_rows = []

    def fit(self, X):
        self.fit_rows.append(X[:, 0].astype(int).tolist())
        return self

    def transform(self, X):
        self.transform_rows.append(X[:, 0].astype(int).tolist())
        return X


class MeanModel:
    def fit(self, X, y):
        self.seen_X_ = X.copy()
        self.mean_ = float(np.mean(y))
        return self

    def predict(self, X):
        self.predict_X_ = X.copy()
        return np.full(len(X), self.mean_)


def mse(y_true, y_pred):
    return float(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2))


def shifted_data(seed=0, n=120):
    """Two features on very different scales; the last third of rows is shifted."""
    rng = np.random.default_rng(seed)
    X = np.column_stack([rng.normal(0, 1, n), rng.normal(0, 1000, n)])
    X[2 * n // 3:] += np.array([3.0, 4000.0])
    y = X[:, 0] + X[:, 1] / 1000 + rng.normal(0, 0.1, n)
    idx = np.arange(n)
    folds = [(np.setdiff1d(idx, part).tolist(), part.tolist()) for part in np.array_split(idx, 3)]
    return X, y, folds


class TestPipelineCV(unittest.TestCase):
    def test_fit_chains_steps_and_returns_self(self):
        model = MeanModel()
        pipe = Pipeline([AddOne(), AddOne()], model)
        X = np.array([[0.0], [1.0]])
        self.assertIs(pipe.fit(X, np.array([2.0, 4.0])), pipe)
        np.testing.assert_allclose(model.seen_X_, X + 2.0)

    def test_predict_transforms_without_refitting(self):
        spy, model = Spy(), MeanModel()
        pipe = Pipeline([spy, AddOne()], model)
        pipe.fit(np.arange(4.0)[:, None], np.array([1.0, 2.0, 3.0, 4.0]))
        np.testing.assert_allclose(pipe.predict(np.array([[7.0], [9.0]])), [2.5, 2.5])
        self.assertEqual(spy.fit_rows, [[0, 1, 2, 3]])
        self.assertEqual(spy.transform_rows, [[0, 1, 2, 3], [7, 9]])
        np.testing.assert_allclose(model.predict_X_, [[8.0], [10.0]])

    def test_scaler_is_fitted_on_training_rows_only(self):
        spy = Spy()
        X = np.arange(6.0)[:, None]
        y = np.arange(6.0)
        folds = [([0, 1, 2, 3], [4, 5]), ([2, 3, 4, 5], [0, 1])]
        cross_val_score(Pipeline([spy], MeanModel()), X, y, folds, mse)
        self.assertEqual(spy.fit_rows, [[0, 1, 2, 3], [2, 3, 4, 5]])

    def test_hand_computed_scores(self):
        X = np.arange(6.0)[:, None]
        y = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
        folds = [([0, 1, 2, 3], [4, 5]), ([2, 3, 4, 5], [0, 1])]
        # Fold 1: mean 3 -> ((8-3)^2 + (10-3)^2) / 2 = 37.  Fold 2: mean 7 -> (49 + 25) / 2 = 37.
        scores = cross_val_score(Pipeline([], MeanModel()), X, y, folds, mse)
        self.assertEqual(len(scores), 2)
        np.testing.assert_allclose(scores, [37.0, 37.0])

    def test_matches_manual_per_fold_scaling(self):
        X, y, folds = shifted_data(1)
        scores = cross_val_score(Pipeline([StandardScaler()], KNNRegressor(3)), X, y, folds, mse)
        for (tr, va), score in zip(folds, scores):
            scaler = StandardScaler().fit(X[tr])
            knn = KNNRegressor(3).fit(scaler.transform(X[tr]), y[tr])
            self.assertAlmostEqual(score, mse(y[va], knn.predict(scaler.transform(X[va]))), places=9)

    def test_leaky_prefitted_scaler_gives_a_different_score(self):
        X, y, folds = shifted_data(2)
        honest = cross_val_score(Pipeline([StandardScaler()], KNNRegressor(3)), X, y, folds, mse)
        leaky = cross_val_score(Pipeline([FrozenScaler(X)], KNNRegressor(3)), X, y, folds, mse)
        self.assertGreater(abs(np.mean(honest) - np.mean(leaky)), 1e-3)

    def test_rejects_no_folds(self):
        with self.assertRaises(ValueError):
            cross_val_score(Pipeline([], MeanModel()), np.zeros((3, 1)), np.zeros(3), [], mse)


if __name__ == "__main__":
    unittest.main(verbosity=2)
