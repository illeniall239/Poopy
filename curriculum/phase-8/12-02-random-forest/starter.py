class RandomForest:
    def __init__(
        self,
        n_trees: int = 25,
        max_features: int | None = None,
        max_depth: int | None = None,
        min_samples: int = 2,
        seed: int = 0,
    ):
        """Store the settings; fit() sets self.trees to a list of nested-dict trees."""
        raise NotImplementedError

    def fit(self, X: list[list[float]], y: list) -> "RandomForest":
        """Grow n_trees Gini trees, each on a bootstrap sample with a random feature subset at every split; return self."""
        raise NotImplementedError

    def predict(self, X: list[list[float]]) -> list:
        """Majority vote of the trees for each row (ties to the smallest label)."""
        raise NotImplementedError
