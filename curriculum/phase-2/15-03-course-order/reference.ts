// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function courseOrder(numCourses: number, prerequisites: [number, number][]): number[] {
  const unlocks: number[][] = Array.from({ length: numCourses }, () => []);
  const inDegree = new Array<number>(numCourses).fill(0);
  for (const [course, required] of prerequisites) {
    unlocks[required].push(course);
    inDegree[course]++;
  }
  const order: number[] = [];
  for (let c = 0; c < numCourses; c++) if (inDegree[c] === 0) order.push(c);
  for (let head = 0; head < order.length; head++) {
    for (const next of unlocks[order[head]]) {
      if (--inDegree[next] === 0) order.push(next);
    }
  }
  return order.length === numCourses ? order : [];
}
