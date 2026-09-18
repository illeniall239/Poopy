# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def days_until_warmer(temps: list[int]) -> list[int]:
    answer = [0] * len(temps)
    waiting: list[int] = []
    for i, temp in enumerate(temps):
        while waiting and temps[waiting[-1]] < temp:
            day = waiting.pop()
            answer[day] = i - day
        waiting.append(i)
    return answer
