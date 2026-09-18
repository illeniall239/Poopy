# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def find_seat(seat_number: int, seats_per_row: int) -> dict[str, int]:
    index = seat_number - 1
    return {"row": index // seats_per_row + 1, "column": index % seats_per_row + 1}
