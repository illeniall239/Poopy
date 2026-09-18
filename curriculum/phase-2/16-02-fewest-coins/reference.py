# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def fewest_coins(coins: list[int], amount: int) -> int:
    fewest = [0] + [math.inf] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and fewest[x - c] + 1 < fewest[x]:
                fewest[x] = fewest[x - c] + 1
    return -1 if fewest[amount] == math.inf else int(fewest[amount])
