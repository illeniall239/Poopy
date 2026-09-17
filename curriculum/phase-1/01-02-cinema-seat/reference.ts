// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Seat = { row: number; column: number };

export function findSeat(seatNumber: number, seatsPerRow: number): Seat {
  const index = seatNumber - 1;
  return { row: Math.floor(index / seatsPerRow) + 1, column: (index % seatsPerRow) + 1 };
}
