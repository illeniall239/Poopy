// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function daysUntilWarmer(temps: number[]): number[] {
  const answer = new Array<number>(temps.length).fill(0);
  const waiting: number[] = [];
  for (let i = 0; i < temps.length; i++) {
    while (waiting.length > 0 && temps[waiting[waiting.length - 1]] < temps[i]) {
      const day = waiting.pop() as number;
      answer[day] = i - day;
    }
    waiting.push(i);
  }
  return answer;
}
