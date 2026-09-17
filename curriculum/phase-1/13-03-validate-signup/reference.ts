// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type SignupForm = { username: string; email: string; password: string; confirmPassword: string };
export type Field = "username" | "email" | "password" | "confirmPassword";
export type FieldError = { field: Field; message: string };
export type ValidationResult = { valid: true } | { valid: false; errors: FieldError[] };

function isLetter(ch: string): boolean {
  return (ch >= "a" && ch <= "z") || (ch >= "A" && ch <= "Z");
}

function isDigit(ch: string): boolean {
  return ch >= "0" && ch <= "9";
}

function checkUsername(raw: string): string | undefined {
  const username = raw.trim();
  if (username === "") return "Username is required";
  if (username.length < 3 || username.length > 20) return "Username must be 3 to 20 characters";
  for (const ch of username) {
    if (!isLetter(ch) && !isDigit(ch) && ch !== "_") return "Username may only contain letters, digits and underscores";
  }
  return undefined;
}

function checkEmail(raw: string): string | undefined {
  const email = raw.trim();
  if (email === "") return "Email is required";
  const parts = email.split("@");
  const valid =
    !email.includes(" ") &&
    parts.length === 2 &&
    parts[0].length > 0 &&
    parts[1].slice(1, -1).includes(".");
  return valid ? undefined : "Email is not valid";
}

function checkPassword(password: string): string | undefined {
  if (password.length < 8) return "Password must be at least 8 characters";
  if (!password.split("").some(isDigit)) return "Password must contain a digit";
  if (!password.split("").some(isLetter)) return "Password must contain a letter";
  return undefined;
}

export function validateSignup(form: SignupForm): ValidationResult {
  const errors: FieldError[] = [];
  const add = (field: Field, message: string | undefined) => {
    if (message !== undefined) errors.push({ field, message });
  };
  add("username", checkUsername(form.username));
  add("email", checkEmail(form.email));
  add("password", checkPassword(form.password));
  add("confirmPassword", form.confirmPassword === form.password ? undefined : "Passwords do not match");
  return errors.length === 0 ? { valid: true } : { valid: false, errors };
}
