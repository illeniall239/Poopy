import { test } from "node:test";
import assert from "node:assert/strict";
import { SparseMatrix } from "./solution.ts";

test("a new matrix is all zeros", () => {
  const m = new SparseMatrix(3, 4);
  assert.equal(m.get(0, 0), 0);
  assert.equal(m.get(2, 3), 0);
  assert.equal(m.nonZeroCount(), 0);
});

test("set and get keep rows and columns apart", () => {
  const m = new SparseMatrix(2, 2);
  m.set(0, 1, 5);
  m.set(1, 0, -7);
  assert.deepEqual([m.get(0, 0), m.get(0, 1), m.get(1, 0), m.get(1, 1)], [0, 5, -7, 0]);
  assert.equal(m.nonZeroCount(), 2);
});

test("overwriting a cell doesn't add to the count", () => {
  const m = new SparseMatrix(1, 1);
  m.set(0, 0, 3);
  m.set(0, 0, 4);
  assert.equal(m.get(0, 0), 4);
  assert.equal(m.nonZeroCount(), 1);
});

test("setting 0 removes a stored cell and ignores an empty one", () => {
  const m = new SparseMatrix(2, 2);
  m.set(1, 1, 9);
  m.set(1, 1, 0);
  m.set(0, 0, 0);
  assert.equal(m.get(1, 1), 0);
  assert.equal(m.nonZeroCount(), 0);
});

test("multiplies by a vector", () => {
  const m = new SparseMatrix(2, 3);
  m.set(0, 0, 1);
  m.set(0, 2, 2);
  m.set(1, 1, 3);
  assert.deepEqual(m.multiplyVector([4, 5, 6]), [16, 15]);
});

test("empty rows give 0 and removed cells don't contribute", () => {
  const m = new SparseMatrix(3, 2);
  m.set(1, 0, -1);
  m.set(1, 1, 2);
  m.set(2, 0, 8);
  m.set(2, 0, 0);
  assert.deepEqual(m.multiplyVector([3, 4]), [0, 5, 0]);
});

test("a matrix with no cells gives a zero vector of length rows", () => {
  assert.deepEqual(new SparseMatrix(4, 1).multiplyVector([7]), [0, 0, 0, 0]);
});

test("200000 x 200000 matrix with 400000 cells in O(rows + non-zeros)", () => {
  const n = 200000;
  const m = new SparseMatrix(n, n);
  for (let i = 0; i < n; i++) {
    m.set(i, i, 2);
    m.set(i, (i + 1) % n, 1);
  }
  assert.equal(m.nonZeroCount(), 2 * n);
  const vector = Array.from({ length: n }, (_, i) => i % 1000);
  const result = m.multiplyVector(vector);
  assert.equal(result.length, n);
  let wrong = 0;
  for (let i = 0; i < n; i++) if (result[i] !== 2 * (i % 1000) + ((i + 1) % n) % 1000) wrong++;
  assert.equal(wrong, 0);
});
