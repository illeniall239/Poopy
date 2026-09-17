# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def max_call_depth(calls: dict[str, list[str]], entry: str) -> int:
    finished: dict[str, int] = {}
    on_stack: set[str] = set()

    def depth_from(fn: str) -> int:
        if fn in finished:
            return finished[fn]
        if fn in on_stack:
            return -1
        on_stack.add(fn)
        deepest = 0
        for callee in calls.get(fn, []):
            depth = depth_from(callee)
            if depth == -1:
                return -1
            deepest = max(deepest, depth)
        on_stack.remove(fn)
        finished[fn] = deepest + 1
        return deepest + 1

    return depth_from(entry)
