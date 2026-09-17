# Validate a sign-up form

Topic: 13. Errors and input validation
Difficulty: 3 of 3

## Problem

When a form has several mistakes, users want to see all of them at once, not fix one, resubmit, and discover the next. Write `validateSignup(form)` that checks a `SignupForm` and collects every problem.

```ts
type SignupForm = { username: string; email: string; password: string; confirmPassword: string };
type Field = "username" | "email" | "password" | "confirmPassword";
type FieldError = { field: Field; message: string };
type ValidationResult = { valid: true } | { valid: false; errors: FieldError[] };
```

Return `{ valid: true }` if there are no problems. Otherwise return `{ valid: false, errors }` where `errors` has at most one error per field, in the field order `username`, `email`, `password`, `confirmPassword`. For each field, report only the first rule it breaks, checking rules in the order listed. `validateSignup` never throws.

**username** (ignore spaces at the start and end):
1. Empty → `Username is required`
2. Fewer than 3 or more than 20 characters → `Username must be 3 to 20 characters`
3. Any character that isn't an English letter (`a`–`z`, `A`–`Z`), a digit or `_` → `Username may only contain letters, digits and underscores`

**email** (ignore spaces at the start and end):
1. Empty → `Email is required`
2. Not valid → `Email is not valid`. An email is valid when it contains no spaces, contains exactly one `@`, has at least one character before the `@`, and the part after the `@` contains a `.` that is neither its first nor its last character.

**password** (spaces count as characters; don't trim):
1. Fewer than 8 characters → `Password must be at least 8 characters`
2. No digit → `Password must contain a digit`
3. No English letter → `Password must contain a letter`

**confirmPassword**:
1. Not exactly equal to `password` → `Passwords do not match`. Check this even if `password` itself broke a rule.

## Examples

```
validateSignup({ username: "ada_99", email: "ada@example.com", password: "s3cretpass", confirmPassword: "s3cretpass" })
  → { valid: true }

validateSignup({ username: "  ", email: "ada@example", password: "short1", confirmPassword: "short2" })
  → { valid: false, errors: [
      { field: "username", message: "Username is required" },
      { field: "email", message: "Email is not valid" },
      { field: "password", message: "Password must be at least 8 characters" },
      { field: "confirmPassword", message: "Passwords do not match" },
    ] }

validateSignup({ username: "ada!", email: "ada@example.com", password: "abcdefgh", confirmPassword: "abcdefgh" })
  → { valid: false, errors: [
      { field: "username", message: "Username may only contain letters, digits and underscores" },
      { field: "password", message: "Password must contain a digit" },
    ] }
```

## Constraints

- Every field is a string of 0 to 200 characters.

## Hints

1. If you `throw` as soon as you find the first problem, what happens to the checks after it? What should you build up instead as you go?
2. Each field's rules are independent of the other fields. Could each field get its own small function that returns either one message or "no problem"? What type would that return?
3. Within one field, how do you make sure only the first broken rule is reported? Think about what an early `return` does.
4. For the email rule, write out a few invalid emails by hand (`@a.com`, `a@b.`, `a@.com`, `a@@b.com`, `a b@c.com`). For each, which part of the rule catches it, and what string operations let you check that part?

## Explain-back

- Why does this function collect errors instead of throwing on the first one, when `parseAge` threw? What's different about who reads the errors?
- A teammate wraps the whole body in `try { ... } catch { return { valid: true } }` "to be safe". What bug does that invite?
- This form is checked at the point it enters the program. Why validate here, once, instead of checking the email again deep inside the code that sends the welcome email?
