import { test } from "node:test";
import assert from "node:assert/strict";
import { validateSignup } from "./solution.ts";

const good = { username: "ada_99", email: "ada@example.com", password: "s3cretpass", confirmPassword: "s3cretpass" };

test("a correct form is valid", () => {
  assert.deepEqual(validateSignup(good), { valid: true });
});

test("surrounding spaces in username and email are ignored", () => {
  assert.deepEqual(validateSignup({ ...good, username: "  ada ", email: " ada@example.com  " }), { valid: true });
});

test("reports every broken field at once, in field order", () => {
  assert.deepEqual(
    validateSignup({ username: "  ", email: "ada@example", password: "short1", confirmPassword: "short2" }),
    {
      valid: false,
      errors: [
        { field: "username", message: "Username is required" },
        { field: "email", message: "Email is not valid" },
        { field: "password", message: "Password must be at least 8 characters" },
        { field: "confirmPassword", message: "Passwords do not match" },
      ],
    },
  );
});

test("only the first broken rule per field is reported", () => {
  assert.deepEqual(
    validateSignup({ ...good, username: "a!", password: "abc", confirmPassword: "abc" }),
    {
      valid: false,
      errors: [
        { field: "username", message: "Username must be 3 to 20 characters" },
        { field: "password", message: "Password must be at least 8 characters" },
      ],
    },
  );
});

test("username rules", () => {
  const messageFor = (username: string) => {
    const result = validateSignup({ ...good, username });
    return result.valid ? undefined : result.errors[0].message;
  };
  assert.equal(messageFor("ab"), "Username must be 3 to 20 characters");
  assert.equal(messageFor("a".repeat(21)), "Username must be 3 to 20 characters");
  assert.equal(messageFor("a".repeat(20)), undefined);
  assert.equal(messageFor("ada lovelace"), "Username may only contain letters, digits and underscores");
  assert.equal(messageFor("adé"), "Username may only contain letters, digits and underscores");
});

test("email rules", () => {
  const messageFor = (email: string) => {
    const result = validateSignup({ ...good, email });
    return result.valid ? undefined : result.errors[0].message;
  };
  assert.equal(messageFor(""), "Email is required");
  assert.equal(messageFor("a@b.co"), undefined);
  for (const bad of ["@a.com", "a@b.", "a@.com", "a@@b.com", "a@b@c.com", "a b@c.com", "abc.com", "a@bcom"]) {
    assert.equal(messageFor(bad), "Email is not valid", bad);
  }
});

test("password rules, and confirm is checked against the password as typed", () => {
  const errorsFor = (password: string, confirmPassword: string) => {
    const result = validateSignup({ ...good, password, confirmPassword });
    return result.valid ? [] : result.errors;
  };
  assert.deepEqual(errorsFor("abcdefgh", "abcdefgh"), [{ field: "password", message: "Password must contain a digit" }]);
  assert.deepEqual(errorsFor("12345678", "12345678"), [{ field: "password", message: "Password must contain a letter" }]);
  assert.deepEqual(errorsFor("pass word1", "pass word1"), []);
  assert.deepEqual(errorsFor("s3cretpass", "s3cretpass "), [{ field: "confirmPassword", message: "Passwords do not match" }]);
});
