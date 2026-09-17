import { test } from "node:test";
import assert from "node:assert/strict";
import { pick, applyPatch } from "./solution.ts";

const makeProfile = () => ({ id: 7, name: "Ana", email: "ana@example.com", theme: "dark" });

test("pick keeps only the listed keys", () => {
  assert.deepEqual(pick(makeProfile(), ["name", "theme"]), { name: "Ana", theme: "dark" });
});

test("pick with no keys gives an empty object", () => {
  assert.deepEqual(pick(makeProfile(), []), {});
});

test("pick with a repeated key includes it once", () => {
  assert.deepEqual(pick(makeProfile(), ["id", "id"]), { id: 7 });
});

test("pick keeps falsy values", () => {
  assert.deepEqual(pick({ count: 0, on: false, label: "" }, ["count", "on", "label"]), { count: 0, on: false, label: "" });
});

test("pick does not change the object", () => {
  const profile = makeProfile();
  pick(profile, ["name"]);
  assert.deepEqual(profile, makeProfile());
});

test("applyPatch replaces patched keys", () => {
  assert.deepEqual(applyPatch(makeProfile(), { theme: "light", name: "Ana B" }), {
    id: 7, name: "Ana B", email: "ana@example.com", theme: "light",
  });
});

test("applyPatch ignores undefined values", () => {
  assert.deepEqual(applyPatch(makeProfile(), { name: undefined }), makeProfile());
});

test("applyPatch keeps falsy patch values that are not undefined", () => {
  assert.deepEqual(applyPatch({ count: 5, on: true }, { count: 0, on: false }), { count: 0, on: false });
});

test("applyPatch returns a new object and changes neither input", () => {
  const profile = makeProfile();
  const patch = { theme: "light" };
  const result = applyPatch(profile, patch);
  assert.notEqual(result, profile);
  assert.deepEqual(profile, makeProfile());
  assert.deepEqual(patch, { theme: "light" });
});
