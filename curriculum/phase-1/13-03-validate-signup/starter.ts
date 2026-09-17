export type SignupForm = { username: string; email: string; password: string; confirmPassword: string };
export type Field = "username" | "email" | "password" | "confirmPassword";
export type FieldError = { field: Field; message: string };
export type ValidationResult = { valid: true } | { valid: false; errors: FieldError[] };

export function validateSignup(form: SignupForm): ValidationResult {
  throw new Error("Not implemented");
}
