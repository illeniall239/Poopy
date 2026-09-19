import random


def augment_flip_crop(img: list[list[float]], rng: random.Random, crop: int) -> list[list[float]]:
    """Randomly flip img horizontally (p = 0.5), then return a random crop x crop window of it."""
    raise NotImplementedError
