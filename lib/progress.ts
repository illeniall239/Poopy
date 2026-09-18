// Pure rules for Learned, retries, Spaced Reviews and the daily Session plan. No I/O, so it's testable.
import type { Topic } from "./curriculum.ts";

export type ExerciseState = {
  exercise_id: string;
  code: string | null;
  hints_shown: number;
  worked_example: number; // 0/1: a Worked Example was shown (the Exercise then Needed Help)
  tests_passed_at: string | null;
  clean_pass: number; // 0/1: tests passed with no hints and no Worked Example
  explain_passed_at: string | null;
  retry_due: string | null; // YYYY-MM-DD: when a helped Exercise comes back
  plan_done_at?: string | null; // the Learner's plan was checked by the Tutor; the editor is locked until then
  plan_text?: string | null; // the Learner's final plan, shown beside the editor
};

export type TopicState = { topic_id: string; teach_done_at: string | null; learned_at: string | null; practice_passed_at?: string | null };
export type Review = { topic_id: string; due_date: string; step: number; last_done: string | null };

export type ExerciseStatus = "new" | "in_progress" | "needs_explain" | "waiting_retry" | "retry_due" | "done";

export const RETRY_AFTER_DAYS = 3;
export const REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60];

export function addDays(date: string, days: number): string {
  const d = new Date(`${date}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

export function localToday(now = new Date()): string {
  const offset = now.getTimezoneOffset() * 60_000;
  return new Date(now.getTime() - offset).toISOString().slice(0, 10);
}

export function exerciseStatus(s: ExerciseState | undefined, today: string): ExerciseStatus {
  if (!s) return "new";
  if (s.tests_passed_at && !s.explain_passed_at) return "needs_explain";
  if (s.clean_pass && s.explain_passed_at) return "done";
  if (s.retry_due) return s.retry_due <= today ? "retry_due" : "waiting_retry";
  return s.code === null ? "new" : "in_progress";
}

// What changes when the tests pass. A pass that used hints or a Worked Example schedules a clean retry.
export function onTestsPassed(s: ExerciseState, now: string, today: string): ExerciseState {
  const clean = s.hints_shown === 0 && !s.worked_example;
  return {
    ...s,
    tests_passed_at: now,
    clean_pass: clean ? 1 : 0,
    retry_due: clean ? null : addDays(today, RETRY_AFTER_DAYS),
  };
}

// Starting a due retry: fresh plan, fresh code, no hints, no Worked Example. retry_due stays set until a clean pass clears it.
export function startRetry(s: ExerciseState, starter: string): ExerciseState {
  return { ...s, code: starter, hints_shown: 0, worked_example: 0, tests_passed_at: null, clean_pass: 0, plan_done_at: null, plan_text: null };
}

// A Topic with in-app Exercises is Learned when they're all done; a Topic practised in the Learner's own project
// (Phases 3+) is Learned when a Project Review of that practice passes.
export const needsProjectReview = (topic: Topic) => topic.exerciseIds.length === 0 && !!topic.practice;

export function isTopicLearned(topic: Topic, topicState: TopicState | undefined, states: Map<string, ExerciseState>, today: string) {
  if (!topicState?.teach_done_at) return false;
  if (needsProjectReview(topic)) return !!topicState.practice_passed_at;
  return topic.exerciseIds.every((id) => exerciseStatus(states.get(id), today) === "done");
}


export function reviewAfter(review: Review, passed: boolean, today: string): Review {
  const step = passed ? Math.min(review.step + 1, REVIEW_INTERVALS.length - 1) : 0;
  return { ...review, step, due_date: addDays(today, REVIEW_INTERVALS[step]), last_done: today };
}

export function firstReview(topicId: string, today: string): Review {
  return { topic_id: topicId, step: 0, due_date: addDays(today, REVIEW_INTERVALS[0]), last_done: null };
}

export type PlanItem =
  | { kind: "review"; topicId: string }
  | { kind: "retry"; exerciseId: string }
  | { kind: "teach"; topicId: string }
  | { kind: "exercise"; exerciseId: string; status: ExerciseStatus }
  | { kind: "practice"; topicId: string };

// The fixed daily loop: due Spaced Reviews → due retries → the current Topic (teach, then its Exercises).
// The "current Topic" is the first one not Learned that still has something to do today; a Topic whose
// remaining Exercises are all waiting for a retry date lets the Learner move on to the next Topic.
export function planToday(
  topics: Topic[],
  topicStates: Map<string, TopicState>,
  exerciseStates: Map<string, ExerciseState>,
  reviews: Review[],
  today: string,
): PlanItem[] {
  const plan: PlanItem[] = [];
  for (const r of reviews) if (r.due_date <= today && r.last_done !== today) plan.push({ kind: "review", topicId: r.topic_id });
  for (const t of topics)
    for (const id of t.exerciseIds)
      if (exerciseStatus(exerciseStates.get(id), today) === "retry_due") plan.push({ kind: "retry", exerciseId: id });

  for (const t of topics) {
    if (isTopicLearned(t, topicStates.get(t.id), exerciseStates, today)) continue;
    if (!topicStates.get(t.id)?.teach_done_at) {
      plan.push({ kind: "teach", topicId: t.id });
      break;
    }
    if (needsProjectReview(t)) {
      plan.push({ kind: "practice", topicId: t.id });
      break;
    }
    const open = t.exerciseIds
      .map((id) => ({ id, status: exerciseStatus(exerciseStates.get(id), today) }))
      .filter((e) => e.status === "new" || e.status === "in_progress" || e.status === "needs_explain");
    if (open.length) {
      for (const e of open) plan.push({ kind: "exercise", exerciseId: e.id, status: e.status });
      break;
    }
    // everything left in this Topic is waiting for a retry date: continue to the next Topic
  }
  return plan;
}
