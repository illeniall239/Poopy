export function average(numbers: number[]): number | undefined {
  if (numbers.length === 0) {
    return undefined;
  }
  let total = 0;
  for (let i = 1; i < numbers.length; i++) {
    total += numbers[i];
  }
  return Math.round(total / numbers.length);
}
