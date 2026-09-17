// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

export function area(shape: Shape): number {
  if (shape.kind === "circle") return Math.PI * shape.radius * shape.radius;
  if (shape.kind === "rectangle") return shape.width * shape.height;
  return (shape.base * shape.height) / 2;
}
