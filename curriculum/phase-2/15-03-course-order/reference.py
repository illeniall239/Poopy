# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    unlocks: list[list[int]] = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    for course, required in prerequisites:
        unlocks[required].append(course)
        in_degree[course] += 1
    order = [c for c in range(num_courses) if in_degree[c] == 0]
    head = 0
    while head < len(order):
        for nxt in unlocks[order[head]]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                order.append(nxt)
        head += 1
    return order if len(order) == num_courses else []
