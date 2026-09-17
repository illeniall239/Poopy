"use server";
// Everything the Learner does that changes progress. Streaming Tutor replies live in app/api/chat/route.ts.
import { revalidatePath } from "next/cache";
import { getExercise, getTopic, loadCurriculum } from "@/lib/curriculum.ts";
import {
  addMessage, allReviews, allTopicStates, allExerciseStates, clearThread, getExerciseState, getMessages, getSetting,
  markTopic, saveExerciseState, saveReview, setSetting,
} from "@/lib/db.ts";
import { jsonReply, settingsDefaults } from "@/lib/llm.ts";
import { runTests } from "@/lib/runner.ts";
import { currentLanguage, isLanguage } from "@/lib/languages.ts";
import {
  exerciseStatus, firstReview, isTopicLearned, localToday, onTestsPassed, reviewAfter, startRetry as retryState,
  type ExerciseState,
} from "@/lib/progress.ts";
import {
  gradeExplainPrompt, gradeReviewPrompt, gradeSchema, reviewQuestionPrompt, reviewQuestionSchema, type Grade,
  PLAN_READY,
} from "@/lib/tutor.ts";

function requireExercise(id: string) {
  const ex = getExercise(id);
  if (!ex) throw new Error(`Unknown exercise ${id}`);
  return ex;
}

function stateOf(id: string): ExerciseState {
  return getExerciseState(id) ?? {
    exercise_id: id, code: null, hints_shown: 0, worked_example: 0, tests_passed_at: null, clean_pass: 0, explain_passed_at: null, retry_due: null, plan_done_at: null, plan_text: null,
  };
}

function checkTopicLearned(topicId: string) {
  const topic = getTopic(topicId);
  if (!topic) return false;
  const today = localToday();
  if (!isTopicLearned(topic, allTopicStates().get(topicId), allExerciseStates(), today)) return false;
  markTopic(topicId, "learned_at");
  if (!allReviews().some((r) => r.topic_id === topicId)) saveReview(firstReview(topicId, today));
  return true;
}

export async function saveCode(exerciseId: string, code: string) {
  requireExercise(exerciseId);
  saveExerciseState({ ...stateOf(exerciseId), code });
}

export async function markPlanDone(exerciseId: string) {
  requireExercise(exerciseId);
  const state = stateOf(exerciseId);
  if (state.plan_done_at) return state.plan_text ?? null;
  const thread = getMessages(`plan:${exerciseId}`);
  const approvedAt = thread.findLastIndex((m) => m.role === "tutor" && m.content.includes(PLAN_READY));
  if (approvedAt < 0) throw new Error("Finish the planning session first: the Tutor hasn't approved your plan yet.");
  const plan = thread.slice(0, approvedAt).findLast((m) => m.role === "learner")?.content ?? null;
  saveExerciseState({ ...state, plan_done_at: new Date().toISOString(), plan_text: plan });
  return plan;
}

export async function runExercise(exerciseId: string, code: string) {
  const ex = requireExercise(exerciseId);
  let state: ExerciseState = { ...stateOf(exerciseId), code };
  if (!state.plan_done_at) throw new Error("Write your plan with the Tutor first.");
  const language = currentLanguage(ex);
  const run = await runTests(code, ex.languages[language]!.test, language);
  if (run.passed && !state.tests_passed_at) state = onTestsPassed(state, new Date().toISOString(), localToday());
  saveExerciseState(state);
  const topicLearned = run.passed ? checkTopicLearned(ex.topicId) : false;
  revalidatePath("/");
  return { ...run, status: exerciseStatus(state, localToday()), topicLearned };
}

export async function showNextHint(exerciseId: string) {
  const ex = requireExercise(exerciseId);
  const state = stateOf(exerciseId);
  const hints_shown = Math.min(state.hints_shown + 1, ex.hints.length);
  saveExerciseState({ ...state, hints_shown });
  return ex.hints.slice(0, hints_shown);
}

export async function startRetry(exerciseId: string) {
  const ex = requireExercise(exerciseId);
  saveExerciseState(retryState(stateOf(exerciseId), ex.languages[currentLanguage(ex)]!.starter));
  clearThread(`plan:${exerciseId}`);
  clearThread(`exercise:${exerciseId}`);
  clearThread(`worked:${exerciseId}`);
  revalidatePath("/");
}

export async function finishExplaining(exerciseId: string): Promise<Grade & { topicLearned: boolean; provider: string; status: string }> {
  const ex = requireExercise(exerciseId);
  const state = stateOf(exerciseId);
  if (!state.tests_passed_at || !state.code) throw new Error("Pass the tests before explaining.");
  const history = getMessages(`explain:${exerciseId}`);
  if (!history.some((m) => m.role === "learner")) {
    return { passed: false, feedback: "Answer the Tutor's questions first.", misconceptions: [], topicLearned: false, provider: "none", status: "needs_explain" };
  }
  const p = gradeExplainPrompt(ex, state.code, history);
  const { value, provider } = await jsonReply<Grade>(p.system, p.messages, gradeSchema);
  let saved = state;
  if (value.passed) {
    saved = { ...state, explain_passed_at: new Date().toISOString() };
    saveExerciseState(saved);
  } else {
    clearThread(`explain:${exerciseId}`); // a fresh round of questions; the feedback is shown to the Learner above it
  }
  const topicLearned = value.passed ? checkTopicLearned(ex.topicId) : false;
  revalidatePath("/");
  return { ...value, topicLearned, provider, status: exerciseStatus(saved, localToday()) };
}

export async function markTeachDone(topicId: string) {
  if (!getTopic(topicId)) throw new Error(`Unknown topic ${topicId}`);
  markTopic(topicId, "teach_done_at");
  revalidatePath("/");
}

export async function getReviewQuestion(topicId: string) {
  const topic = getTopic(topicId);
  if (!topic) throw new Error(`Unknown topic ${topicId}`);
  const thread = `review:${topicId}:${localToday()}`;
  const existing = getMessages(thread).find((m) => m.role === "tutor");
  if (existing) return existing.content;
  const p = reviewQuestionPrompt(topic);
  const { value, provider } = await jsonReply<{ question: string }>(p.system, p.messages, reviewQuestionSchema);
  addMessage(thread, "tutor", value.question, provider);
  return value.question;
}

export async function answerReview(topicId: string, answer: string) {
  const topic = getTopic(topicId);
  if (!topic) throw new Error(`Unknown topic ${topicId}`);
  const review = allReviews().find((r) => r.topic_id === topicId);
  if (!review) throw new Error("This Topic has no Spaced Review yet.");
  const today = localToday();
  const thread = `review:${topicId}:${today}`;
  const question = getMessages(thread).find((m) => m.role === "tutor")?.content;
  if (!question) throw new Error("Load the question first.");
  addMessage(thread, "learner", answer);
  const p = gradeReviewPrompt(topic, question, answer);
  const { value, provider } = await jsonReply<Grade>(p.system, p.messages, gradeSchema);
  addMessage(thread, "tutor", `**${value.passed ? "Passed" : "Not yet"}.** ${value.feedback}`, provider);
  const next = reviewAfter(review, value.passed, today);
  saveReview(next);
  revalidatePath("/");
  return { ...value, nextDue: next.due_date };
}

export async function setLanguage(language: string) {
  if (!isLanguage(language)) throw new Error("Unknown language");
  setSetting("language", language);
  revalidatePath("/", "layout");
}

export async function saveSettings(formData: FormData) {
  for (const key of Object.keys(settingsDefaults) as (keyof typeof settingsDefaults)[]) {
    const value = String(formData.get(key) ?? "").trim();
    if (!value) continue;
    if (key === "providerMode" && !["auto", "claude", "ollama"].includes(value)) continue;
    if (key === "language" && !isLanguage(value)) continue;
    if (key === "ollamaUrl" && !/^https?:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/.test(value)) continue; // keep model traffic on this machine
    setSetting(key, value);
  }
  revalidatePath("/settings");
}

// Used by the recap: a plain-text summary of today's work.
export async function todaySummary() {
  const today = localToday();
  const { topics, exercises } = loadCurriculum();
  const topicStates = allTopicStates();
  const lines: string[] = [];
  for (const t of topics) {
    const ts = topicStates.get(t.id);
    if (ts?.teach_done_at && localToday(new Date(ts.teach_done_at.replace(" ", "T") + "Z")) === today) lines.push(`Learned the concepts of Topic ${t.id} ${t.title}`);
  }
  for (const s of allExerciseStates().values()) {
    if (s.tests_passed_at && localToday(new Date(s.tests_passed_at)) === today) {
      lines.push(`Passed Exercise "${exercises.get(s.exercise_id)?.title}"${s.clean_pass ? "" : " with help"}`);
    }
  }
  for (const r of allReviews()) if (r.last_done === today) lines.push(`Did the Spaced Review for Topic ${r.topic_id}`);
  return lines.length ? lines.map((l) => `- ${l}`).join("\n") : "- Nothing recorded yet today.";
}
