// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type Strength = { score: number; label: "weak" | "medium" | "strong" };

function isLower(ch: string): boolean {
  return ch >= "a" && ch <= "z";
}

function isUpper(ch: string): boolean {
  return ch >= "A" && ch <= "Z";
}

function isDigit(ch: string): boolean {
  return ch >= "0" && ch <= "9";
}

export function hasLowercase(password: string): boolean {
  for (const ch of password) {
    if (isLower(ch)) return true;
  }
  return false;
}

export function hasUppercase(password: string): boolean {
  for (const ch of password) {
    if (isUpper(ch)) return true;
  }
  return false;
}

export function hasDigit(password: string): boolean {
  for (const ch of password) {
    if (isDigit(ch)) return true;
  }
  return false;
}

export function hasSymbol(password: string): boolean {
  for (const ch of password) {
    if (!isLower(ch) && !isUpper(ch) && !isDigit(ch)) return true;
  }
  return false;
}

export function passwordStrength(password: string): Strength {
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (hasLowercase(password)) score++;
  if (hasUppercase(password)) score++;
  if (hasDigit(password)) score++;
  if (hasSymbol(password)) score++;

  if (score >= 5) return { score, label: "strong" };
  if (score >= 3) return { score, label: "medium" };
  return { score, label: "weak" };
}
