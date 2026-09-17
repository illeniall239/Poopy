export type Strength = { score: number; label: "weak" | "medium" | "strong" };

export function hasLowercase(password: string): boolean {
  throw new Error("Not implemented");
}

export function hasUppercase(password: string): boolean {
  throw new Error("Not implemented");
}

export function hasDigit(password: string): boolean {
  throw new Error("Not implemented");
}

export function hasSymbol(password: string): boolean {
  throw new Error("Not implemented");
}

export function passwordStrength(password: string): Strength {
  throw new Error("Not implemented");
}
