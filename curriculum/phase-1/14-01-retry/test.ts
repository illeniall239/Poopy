import { test } from "node:test";
import assert from "node:assert/strict";
import { retry } from "./solution.ts";

// Returns a task that rejects `failures` times (with a new Error each time), then resolves "ok".
function flakyTask(failures: number) {
  const errors: Error[] = [];
  const task = async () => {
    await new Promise((resolve) => setTimeout(resolve, 1));
    if (errors.length < failures) {
      const error = new Error(`failure ${errors.length + 1}`);
      errors.push(error);
      throw error;
    }
    return "ok";
  };
  return { task, errors };
}

test("resolves on the first try without retrying", async () => {
  let calls = 0;
  const result = await retry(async () => {
    calls++;
    return "first";
  }, 5);
  assert.equal(result, "first");
  assert.equal(calls, 1);
});

test("retries after rejections until one succeeds", async () => {
  const flaky = flakyTask(2);
  assert.equal(await retry(flaky.task, 3), "ok");
  assert.equal(flaky.errors.length, 2);
});

test("rejects with the last attempt's error when every attempt fails", async () => {
  const flaky = flakyTask(10);
  await assert.rejects(retry(flaky.task, 3), (error) => error === flaky.errors[2]);
  assert.equal(flaky.errors.length, 3);
});

test("one attempt means no retries", async () => {
  const flaky = flakyTask(1);
  await assert.rejects(retry(flaky.task, 1), { message: "failure 1" });
  assert.equal(flaky.errors.length, 1);
});

test("maxAttempts below 1 rejects with a RangeError and never calls the task", async () => {
  let calls = 0;
  const task = async () => {
    calls++;
    return "x";
  };
  await assert.rejects(retry(task, 0), { name: "RangeError", message: "maxAttempts must be at least 1" });
  await assert.rejects(retry(task, -2), { name: "RangeError" });
  assert.equal(calls, 0);
});

test("attempts never overlap", async () => {
  let running = 0;
  let maxRunning = 0;
  let calls = 0;
  const task = async () => {
    running++;
    maxRunning = Math.max(maxRunning, running);
    calls++;
    await new Promise((resolve) => setTimeout(resolve, 5));
    running--;
    if (calls < 4) throw new Error("not yet");
    return "done";
  };
  assert.equal(await retry(task, 4), "done");
  assert.equal(maxRunning, 1);
});

test("waits delayMs between attempts", async () => {
  const flaky = flakyTask(10);
  const started = Date.now();
  await assert.rejects(retry(flaky.task, 3, 25));
  assert.ok(Date.now() - started >= 45, "expected two waits of about 25ms");
});
