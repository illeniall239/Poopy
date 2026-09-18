// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function binaryToDecimal(bits: string): number {
  if (bits.length === 0) {
    throw new Error("Binary string is empty");
  }
  for (const ch of bits) {
    if (ch !== "0" && ch !== "1") {
      throw new Error(`Not a binary string: "${bits}"`);
    }
  }

  let result = 0;
  let placeValue = 1;
  for (let i = bits.length - 1; i >= 0; i--) {
    if (bits[i] === "1") {
      result += placeValue;
    }
    placeValue *= 2;
  }
  return result;
}
