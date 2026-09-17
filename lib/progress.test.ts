import { test } from "node:test";
import assert from "node:assert/strict";
import type { Topic } from "./curriculum.ts";
import {
  addDays, exerciseStatus, onTestsPassed, startRetry, planToday, reviewAfter, firstReview,
  type ExerciseState, type TopicState,
} from "./progress.ts";

const blank = (id: string): ExerciseState => ({
  exercise_id: id, code: "x", hints_shown: 0, worked_example: 0, tests_passed_at: null, clean_pass: 0, explain_passed_at: null, retry_due: null,
});
const topic = (n: number, ex: string[]): Topic => ({ id: `1.${n}`, phase: 1, number: n, title: `T${n}`, learnedWhen: "", teach: "", probe: "", practice: "", sources: "", exerciseIds: ex });
const today = "2026-09-17";

test("addDays crosses month ends", () => {
  assert.equal(addDays("2026-09-29", 3), "2026-10-02");
});

test("clean pass then explain-back is done", () => {
  let s = onTestsPassed(blank("a"), "t", today);
  assert.equal(exerciseStatus(s, today), "needs_explain");
  s = { ...s, explain_passed_at: "t" };
  assert.equal(exerciseStatus(s, today), "done");
});

test("a pass with a hint needs explaining, then waits 3 days, then must be redone clean", () => {
  let s = onTestsPassed({ ...blank("a"), hints_shown: 1 }, "t", today);
  assert.equal(s.retry_due, "2026-09-20");
  s = { ...s, explain_passed_at: "t" };
  assert.equal(exerciseStatus(s, today), "waiting_retry");
  assert.equal(exerciseStatus(s, "2026-09-20"), "retry_due");
  s = startRetry(s, "starter");
  assert.equal(s.hints_shown, 0);
  assert.equal(exerciseStatus(s, "2026-09-20"), "retry_due");
  s = onTestsPassed(s, "t2", "2026-09-20");
  assert.equal(exerciseStatus(s, "2026-09-20"), "done");
});

test("a Worked Example counts as help even with no hints", () => {
  const s = onTestsPassed({ ...blank("a"), worked_example: 1 }, "t", today);
  assert.equal(s.clean_pass, 0);
});

test("plan: teach comes before exercises, then exercises of the current topic only", () => {
  const topics = [topic(1, ["a", "b"]), topic(2, ["c"])];
  const noTeach = planToday(topics, new Map(), new Map(), [], today);
  assert.deepEqual(noTeach, [{ kind: "teach", topicId: "1.1" }]);

  const taught = new Map<string, TopicState>([["1.1", { topic_id: "1.1", teach_done_at: "t", learned_at: null }]]);
  const plan = planToday(topics, taught, new Map(), [], today);
  assert.deepEqual(plan.map((p) => p.kind === "exercise" && p.exerciseId), ["a", "b"]);
});

test("plan: a topic waiting only on retries lets the learner move on, and due reviews come first", () => {
  const topics = [topic(1, ["a"]), topic(2, ["c"])];
  const taught = new Map<string, TopicState>([["1.1", { topic_id: "1.1", teach_done_at: "t", learned_at: null }]]);
  const waiting = { ...onTestsPassed({ ...blank("a"), hints_shown: 2 }, "t", today), explain_passed_at: "t" };
  const reviews = [{ topic_id: "1.0", due_date: today, step: 0, last_done: null }];
  const plan = planToday(topics, taught, new Map([["a", waiting]]), reviews, today);
  assert.deepEqual(plan, [{ kind: "review", topicId: "1.0" }, { kind: "teach", topicId: "1.2" }]);
});

test("reviews: pass climbs the interval ladder, fail resets to tomorrow, reviewed today is not due again", () => {
  let r = firstReview("1.1", today);
  assert.equal(r.due_date, "2026-09-18");
  r = reviewAfter(r, true, "2026-09-18");
  assert.equal(r.due_date, "2026-09-21");
  r = reviewAfter(r, false, "2026-09-21");
  assert.deepEqual([r.step, r.due_date], [0, "2026-09-22"]);
  assert.deepEqual(planToday([], new Map(), new Map(), [{ ...r, due_date: "2026-09-21" }], "2026-09-21"), []);
});
