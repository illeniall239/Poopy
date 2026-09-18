# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def compress_runs(text: str) -> str:
    result = ""
    i = 0
    while i < len(text):
        ch = text[i]
        count = 0
        while i < len(text) and text[i] == ch:
            count += 1
            i += 1
        result += f"{ch}{count}" if count > 1 else ch
    return result
