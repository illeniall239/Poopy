import { test } from "node:test";
import assert from "node:assert/strict";
import { fetchAll, fetchOneByOne } from "./solution.ts";

const delays: Record<string, number> = { a: 30, b: 10, c: 20, bad: 5, slow: 40 };

// A fake fetchPage that records when each download starts and ends. "bad" rejects.
function fakeFetcher() {
  const log: string[] = [];
  const fetchPage = (url: string) =>
    new Promise<string>((resolve, reject) => {
      log.push(`start ${url}`);
      setTimeout(() => {
        log.push(`end ${url}`);
        if (url === "bad") reject(new Error("download failed: bad"));
        else resolve(`page ${url}`);
      }, delays[url]);
    });
  return { fetchPage, log };
}

test("fetchAll returns pages in input order, not finishing order", async () => {
  const { fetchPage } = fakeFetcher();
  assert.deepEqual(await fetchAll(["a", "b", "c"], fetchPage), ["page a", "page b", "page c"]);
});

test("fetchAll starts every download before any finishes", async () => {
  const { fetchPage, log } = fakeFetcher();
  await fetchAll(["a", "b", "c"], fetchPage);
  assert.deepEqual(log.slice(0, 3), ["start a", "start b", "start c"]);
});

test("fetchAll rejects on failure, but other downloads keep running", async () => {
  const { fetchPage, log } = fakeFetcher();
  await assert.rejects(fetchAll(["slow", "bad"], fetchPage), { message: "download failed: bad" });
  assert.ok(!log.includes("end slow"), "rejects as soon as one download fails");
  await new Promise((resolve) => setTimeout(resolve, 60));
  assert.ok(log.includes("end slow"), "the slow download still finished");
});

test("fetchOneByOne runs downloads strictly one after another", async () => {
  const { fetchPage, log } = fakeFetcher();
  assert.deepEqual(await fetchOneByOne(["a", "b", "c"], fetchPage), ["page a", "page b", "page c"]);
  assert.deepEqual(log, ["start a", "end a", "start b", "end b", "start c", "end c"]);
});

test("fetchOneByOne stops at the first failure", async () => {
  const { fetchPage, log } = fakeFetcher();
  await assert.rejects(fetchOneByOne(["b", "bad", "c"], fetchPage), { message: "download failed: bad" });
  await new Promise((resolve) => setTimeout(resolve, 30));
  assert.deepEqual(log, ["start b", "end b", "start bad", "end bad"]);
});

test("empty list resolves to an empty array without fetching", async () => {
  const { fetchPage, log } = fakeFetcher();
  assert.deepEqual(await fetchAll([], fetchPage), []);
  assert.deepEqual(await fetchOneByOne([], fetchPage), []);
  assert.deepEqual(log, []);
});
