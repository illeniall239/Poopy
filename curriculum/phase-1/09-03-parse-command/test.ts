import { test } from "node:test";
import assert from "node:assert/strict";
import { parseCommand } from "./solution.ts";

test("move command", () => {
  assert.deepEqual(parseCommand("move up 3"), { type: "move", direction: "up", steps: 3 });
});

test("extra spaces and mixed case", () => {
  assert.deepEqual(parseCommand("  MOVE   Left 10 "), { type: "move", direction: "left", steps: 10 });
  assert.deepEqual(parseCommand("Move DOWN 007"), { type: "move", direction: "down", steps: 7 });
});

test("say joins words with single spaces and keeps their case", () => {
  assert.deepEqual(parseCommand("say Hello   there"), { type: "say", message: "Hello there" });
  assert.deepEqual(parseCommand(" SAY move up 3 "), { type: "say", message: "move up 3" });
});

test("quit", () => {
  assert.deepEqual(parseCommand("quit"), { type: "quit" });
  assert.deepEqual(parseCommand("  QUIT "), { type: "quit" });
});

test("bad direction is an error", () => {
  for (const input of ["move north 2", "move Upward 2"]) {
    const result = parseCommand(input);
    assert.equal(result.type, "error", `expected an error for "${input}"`);
    assert.ok(result.type === "error" && result.message.length > 0, `empty error message for "${input}"`);
  }
});

test("steps must be whole digits and at least 1", () => {
  for (const input of ["move up 0", "move up -1", "move up 2.5", "move up two", "move up 3x"]) {
    const result = parseCommand(input);
    assert.equal(result.type, "error", `expected an error for "${input}"`);
    assert.ok(result.type === "error" && result.message.length > 0, `empty error message for "${input}"`);
  }
});

test("wrong number of words is an error", () => {
  for (const input of ["move up", "move up 2 3", "say", "say   ", "quit now"]) {
    const result = parseCommand(input);
    assert.equal(result.type, "error", `expected an error for "${input}"`);
    assert.ok(result.type === "error" && result.message.length > 0, `empty error message for "${input}"`);
  }
});

test("empty and unknown input is an error", () => {
  for (const input of ["", "    ", "jump 3"]) {
    const result = parseCommand(input);
    assert.equal(result.type, "error", `expected an error for "${input}"`);
    assert.ok(result.type === "error" && result.message.length > 0, `empty error message for "${input}"`);
  }
});
