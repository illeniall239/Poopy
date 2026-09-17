import { test } from "node:test";
import assert from "node:assert/strict";
import { sleep, withTimeout } from "./solution.ts";

test("sleep resolves with undefined after the delay", async () => {
  const started = Date.now();
  const result = await sleep(20);
  assert.equal(result, undefined);
  assert.ok(Date.now() - started >= 15);
});

test("resolves with the value when the promise is fast enough", async () => {
  assert.equal(await withTimeout(sleep(5).then(() => "done"), 50), "done");
});

test("rejects with a timeout error when the promise is too slow", async () => {
  await assert.rejects(withTimeout(sleep(50).then(() => "late"), 10), { name: "Error", message: "Timed out after 10ms" });
});

test("does not wait for the slow promise after timing out", async () => {
  const started = Date.now();
  await assert.rejects(withTimeout(sleep(300).then(() => "late"), 10));
  assert.ok(Date.now() - started < 200, "should reject after about 10ms");
});

test("passes through the original rejection", async () => {
  const boom = new Error("boom");
  await assert.rejects(withTimeout(Promise.reject(boom), 50), (error) => error === boom);
});

test("an already-resolved promise wins even with a 0ms timeout", async () => {
  assert.equal(await withTimeout(Promise.resolve("ready"), 0), "ready");
});

test("a late rejection after the timeout is ignored", async () => {
  const late = sleep(20).then((): string => {
    throw new Error("late failure");
  });
  await assert.rejects(withTimeout(late, 5), { message: "Timed out after 5ms" });
  await sleep(40);
});

test("negative ms rejects with a RangeError", async () => {
  await assert.rejects(withTimeout(Promise.resolve("x"), -1), { name: "RangeError", message: "ms must not be negative" });
});
