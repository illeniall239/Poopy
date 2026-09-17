// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function fewestCoins(coins: number[], amount: number): number {
  const fewest = new Array<number>(amount + 1).fill(Infinity);
  fewest[0] = 0;
  for (let x = 1; x <= amount; x++) {
    for (const c of coins) {
      if (c <= x && fewest[x - c] + 1 < fewest[x]) fewest[x] = fewest[x - c] + 1;
    }
  }
  return fewest[amount] === Infinity ? -1 : fewest[amount];
}
