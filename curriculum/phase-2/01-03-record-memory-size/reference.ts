// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
const SIZES: Record<string, number> = { bool: 1, i8: 1, i16: 2, i32: 4, f32: 4, i64: 8, f64: 8, ptr: 8 };

function roundUp(offset: number, multiple: number): number {
  return Math.ceil(offset / multiple) * multiple;
}

export function recordSize(fields: string[]): number {
  let offset = 0;
  let largest = 1;
  for (const field of fields) {
    const size = SIZES[field];
    offset = roundUp(offset, size) + size;
    largest = Math.max(largest, size);
  }
  return roundUp(offset, largest);
}

export function arraySize(fields: string[], count: number): number {
  return recordSize(fields) * count;
}
