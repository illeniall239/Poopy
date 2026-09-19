import random
from typing import Any


def sample_configs(space: dict[str, tuple], n: int, rng: random.Random) -> list[dict[str, Any]]:
    """Draw n random configs from space; "log" ranges are sampled log-uniformly."""
    raise NotImplementedError
