// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
function repeat(symbol: string, times: number): string {
  let result = "";
  for (let i = 0; i < times; i++) result += symbol;
  return result;
}

function digitToRoman(digit: number, one: string, five: string, ten: string): string {
  if (digit === 9) return one + ten;
  if (digit >= 5) return five + repeat(one, digit - 5);
  if (digit === 4) return one + five;
  return repeat(one, digit);
}

export function toRoman(n: number): string {
  if (Math.floor(n) !== n || n < 1 || n > 3999) return "";
  return (
    repeat("M", Math.floor(n / 1000)) +
    digitToRoman(Math.floor(n / 100) % 10, "C", "D", "M") +
    digitToRoman(Math.floor(n / 10) % 10, "X", "L", "C") +
    digitToRoman(n % 10, "I", "V", "X")
  );
}
