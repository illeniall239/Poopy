import { test } from "node:test";
import assert from "node:assert/strict";
import { pipeline, when } from "./solution.ts";

const addOne = (n: number) => n + 1;
const double = (n: number) => n * 2;

test("runs steps left to right", () => {
  assert.equal(pipeline([addOne, double])(3), 8);
  assert.equal(pipeline([double, addOne])(3), 7);
});

test("no steps returns the input unchanged", () => {
  assert.equal(pipeline([])(42), 42);
});

test("each step runs exactly once per call", () => {
  let calls = 0;
  const counted = (n: number) => {
    calls++;
    return n;
  };
  pipeline([counted, addOne, counted])(0);
  assert.equal(calls, 2);
});

test("the returned step can be reused", () => {
  const run = pipeline([addOne, double]);
  assert.equal(run(1), 4);
  assert.equal(run(1), 4);
  assert.equal(run(10), 22);
});

test("changing the steps array afterwards has no effect", () => {
  const steps = [addOne];
  const run = pipeline(steps);
  steps.push(double);
  assert.equal(run(5), 6);
});

test("when runs the step only if the predicate holds", () => {
  const halveEvens = when((n) => n % 2 === 0, (n) => n / 2);
  assert.equal(halveEvens(10), 5);
  assert.equal(halveEvens(7), 7);
});

test("pipelines and when combine", () => {
  const halveEvens = when((n) => n % 2 === 0, (n) => n / 2);
  assert.equal(pipeline([addOne, halveEvens, double])(5), 6);
  assert.equal(pipeline([pipeline([addOne, addOne]), double])(1), 6);
});
