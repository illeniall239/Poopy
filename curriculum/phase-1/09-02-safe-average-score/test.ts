import { test } from "node:test";
import assert from "node:assert/strict";
import { averageScore } from "./solution.ts";

test("all scores present", () => {
  assert.equal(averageScore([{ name: "Ana", score: 80 }, { name: "Ben", score: 90 }]), 85);
});

test("absent score is skipped, not counted as zero", () => {
  assert.equal(averageScore([{ name: "Ana", score: 80 }, { name: "Ben" }]), 80);
});

test("a score of 0 counts", () => {
  assert.equal(averageScore([{ name: "Ana", score: 0 }, { name: "Ben", score: 10 }]), 5);
});

test("null and undefined scores are skipped", () => {
  assert.equal(
    averageScore([
      { name: "Ana", score: null },
      { name: "Ben", score: 40 },
      { name: "Cy", score: undefined },
      { name: "Di", score: 60 },
    ]),
    50,
  );
});

test("no present scores gives null", () => {
  assert.equal(averageScore([{ name: "Ana", score: null }, { name: "Ben" }]), null);
});

test("empty array gives null", () => {
  assert.equal(averageScore([]), null);
});

test("result is not rounded", () => {
  assert.equal(averageScore([{ name: "Ana", score: 1 }, { name: "Ben", score: 2 }]), 1.5);
});

test("all zeros averages to 0, not null", () => {
  assert.equal(averageScore([{ name: "Ana", score: 0 }]), 0);
});

test("does not modify the input", () => {
  const students = [{ name: "Ana", score: 70 }, { name: "Ben" }];
  averageScore(students);
  assert.deepEqual(students, [{ name: "Ana", score: 70 }, { name: "Ben" }]);
});
