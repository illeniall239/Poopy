# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
OPENER_OF = {")": "(", "]": "[", "}": "{"}


def is_balanced(s: str) -> bool:
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in OPENER_OF:
            if not stack or stack.pop() != OPENER_OF[ch]:
                return False
    return not stack
