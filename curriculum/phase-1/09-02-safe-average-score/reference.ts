// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Student = { name: string; score?: number | null };

export function averageScore(students: Student[]): number | null {
  let sum = 0;
  let count = 0;
  for (const student of students) {
    if (typeof student.score === "number") {
      sum += student.score;
      count++;
    }
  }
  return count === 0 ? null : sum / count;
}
