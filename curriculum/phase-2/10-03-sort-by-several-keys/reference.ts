// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type Player = { id: number; name: string; score: number };

export function sortBySeveralKeys(players: Player[]): Player[] {
  return [...players].sort((a, b) => {
    if (a.score !== b.score) return b.score - a.score;
    if (a.name < b.name) return -1;
    if (a.name > b.name) return 1;
    return 0;
  });
}
