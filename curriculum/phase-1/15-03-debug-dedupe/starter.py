def dedupe(items: list[int]) -> list[int]:
    seen = set()
    for i, item in enumerate(items):
        if item in seen:
            del items[i]
        else:
            seen.add(item)
    return items
