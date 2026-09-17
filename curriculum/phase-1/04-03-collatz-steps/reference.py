# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def collatz_steps(n: int) -> dict[str, int]:
    steps = 0
    peak = n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
        if n > peak:
            peak = n
    return {"steps": steps, "peak": peak}
