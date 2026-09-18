// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type Seat = { row: number; column: number };

export function findSeat(seatNumber: number, seatsPerRow: number): Seat {
  const index = seatNumber - 1;
  return { row: Math.floor(index / seatsPerRow) + 1, column: (index % seatsPerRow) + 1 };
}
