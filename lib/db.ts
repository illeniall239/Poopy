// SQLite storage for the Learner's progress. One file: data/poopy.db (back it up with Export in Settings).
import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import type { ExerciseState, Review, TopicState } from "./progress.ts";

const DATA_DIR = join(process.cwd(), "data");

const SCHEMA = `
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS exercise_state (
  exercise_id TEXT PRIMARY KEY,
  code TEXT,
  hints_shown INTEGER NOT NULL DEFAULT 0,
  worked_example INTEGER NOT NULL DEFAULT 0,
  tests_passed_at TEXT,
  clean_pass INTEGER NOT NULL DEFAULT 0,
  explain_passed_at TEXT,
  retry_due TEXT,
  plan_done_at TEXT,
  plan_text TEXT
);
CREATE TABLE IF NOT EXISTS topic_state (topic_id TEXT PRIMARY KEY, teach_done_at TEXT, learned_at TEXT);
CREATE TABLE IF NOT EXISTS reviews (topic_id TEXT PRIMARY KEY, due_date TEXT NOT NULL, step INTEGER NOT NULL, last_done TEXT);
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thread TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('learner', 'tutor')),
  content TEXT NOT NULL,
  provider TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS messages_thread ON messages (thread, id);
CREATE TABLE IF NOT EXISTS mistakes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id TEXT,
  text TEXT NOT NULL,
  source TEXT NOT NULL,
  count INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS sketches (exercise_id TEXT PRIMARY KEY, scene TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE IF NOT EXISTS days (date TEXT PRIMARY KEY, exercise_passed INTEGER NOT NULL DEFAULT 0, kept INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS interviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL,
  language TEXT,
  started_at TEXT NOT NULL DEFAULT (datetime('now')),
  ended_at TEXT,
  code TEXT,
  feedback TEXT
);
CREATE TABLE IF NOT EXISTS project_reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id TEXT NOT NULL,
  folder TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  passed INTEGER NOT NULL,
  result TEXT NOT NULL
);
`;

// One connection per server process; survives Next.js dev hot reloads via globalThis.
const g = globalThis as unknown as { tutorDb?: DatabaseSync };

export function db(): DatabaseSync {
  if (!g.tutorDb) {
    mkdirSync(DATA_DIR, { recursive: true });
    const d = new DatabaseSync(join(DATA_DIR, "poopy.db"));
    d.exec("PRAGMA journal_mode = WAL;");
    d.exec(SCHEMA);
    // Columns added after the first release: add them to databases created before.
    const cols = (d.prepare("PRAGMA table_info(exercise_state)").all() as { name: string }[]).map((c) => c.name);
    if (!cols.includes("plan_done_at")) d.exec("ALTER TABLE exercise_state ADD COLUMN plan_done_at TEXT");
    if (!cols.includes("plan_text")) d.exec("ALTER TABLE exercise_state ADD COLUMN plan_text TEXT");
    const topicCols = (d.prepare("PRAGMA table_info(topic_state)").all() as { name: string }[]).map((c) => c.name);
    if (!topicCols.includes("practice_passed_at")) d.exec("ALTER TABLE topic_state ADD COLUMN practice_passed_at TEXT");
    g.tutorDb = d;
  }
  return g.tutorDb;
}

export type Message = { id: number; thread: string; role: "learner" | "tutor"; content: string; provider: string | null; created_at: string };

export const getSetting = (key: string, fallback: string) =>
  (db().prepare("SELECT value FROM settings WHERE key = ?").get(key) as { value: string } | undefined)?.value ?? fallback;

export const setSetting = (key: string, value: string) =>
  db().prepare("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value").run(key, value);

export const getMessages = (thread: string) =>
  db().prepare("SELECT * FROM messages WHERE thread = ? ORDER BY id").all(thread) as Message[];

export const addMessage = (thread: string, role: Message["role"], content: string, provider: string | null = null) =>
  db().prepare("INSERT INTO messages (thread, role, content, provider) VALUES (?, ?, ?, ?)").run(thread, role, content, provider);

export const clearThread = (thread: string) => db().prepare("DELETE FROM messages WHERE thread = ?").run(thread);

export function getExerciseState(id: string): ExerciseState | undefined {
  return db().prepare("SELECT * FROM exercise_state WHERE exercise_id = ?").get(id) as ExerciseState | undefined;
}

export function saveExerciseState(s: ExerciseState) {
  db().prepare(`INSERT INTO exercise_state (exercise_id, code, hints_shown, worked_example, tests_passed_at, clean_pass, explain_passed_at, retry_due, plan_done_at, plan_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(exercise_id) DO UPDATE SET code = excluded.code, hints_shown = excluded.hints_shown, worked_example = excluded.worked_example,
      tests_passed_at = excluded.tests_passed_at, clean_pass = excluded.clean_pass, explain_passed_at = excluded.explain_passed_at, retry_due = excluded.retry_due,
      plan_done_at = excluded.plan_done_at, plan_text = excluded.plan_text`)
    .run(s.exercise_id, s.code, s.hints_shown, s.worked_example, s.tests_passed_at, s.clean_pass, s.explain_passed_at, s.retry_due, s.plan_done_at ?? null, s.plan_text ?? null);
}

export function allExerciseStates() {
  const rows = db().prepare("SELECT * FROM exercise_state").all() as ExerciseState[];
  return new Map(rows.map((r) => [r.exercise_id, r]));
}

export function allTopicStates() {
  const rows = db().prepare("SELECT * FROM topic_state").all() as TopicState[];
  return new Map(rows.map((r) => [r.topic_id, r]));
}

export function markTopic(topicId: string, column: "teach_done_at" | "learned_at" | "practice_passed_at") {
  db().prepare(`INSERT INTO topic_state (topic_id, ${column}) VALUES (?, datetime('now'))
    ON CONFLICT(topic_id) DO UPDATE SET ${column} = COALESCE(${column}, excluded.${column})`).run(topicId);
}

export const allReviews = () => db().prepare("SELECT * FROM reviews ORDER BY due_date").all() as Review[];

export function saveReview(r: Review) {
  db().prepare(`INSERT INTO reviews (topic_id, due_date, step, last_done) VALUES (?, ?, ?, ?)
    ON CONFLICT(topic_id) DO UPDATE SET due_date = excluded.due_date, step = excluded.step, last_done = excluded.last_done`)
    .run(r.topic_id, r.due_date, r.step, r.last_done);
}

// Full export for backups: every table as JSON.
export function exportAll() {
  const tables = ["settings", "exercise_state", "topic_state", "reviews", "messages", "mistakes", "days", "interviews", "project_reviews", "sketches"];
  return Object.fromEntries(tables.map((t) => [t, db().prepare(`SELECT * FROM ${t}`).all()]));
}

// ---------- Mistake Log ----------
export type Mistake = { id: number; topic_id: string | null; text: string; source: string; count: number; created_at: string; updated_at: string };

// Same wording on the same topic counts up instead of adding a duplicate.
export function logMistake(topicId: string | null, text: string, source: string) {
  const clean = text.trim();
  if (!clean) return;
  const existing = db().prepare("SELECT id FROM mistakes WHERE lower(text) = lower(?) AND topic_id IS ?").get(clean, topicId) as { id: number } | undefined;
  if (existing) db().prepare("UPDATE mistakes SET count = count + 1, source = ?, updated_at = datetime('now') WHERE id = ?").run(source, existing.id);
  else db().prepare("INSERT INTO mistakes (topic_id, text, source) VALUES (?, ?, ?)").run(topicId, clean, source);
}
export const allMistakes = () => db().prepare("SELECT * FROM mistakes ORDER BY count DESC, updated_at DESC").all() as Mistake[];
export const topicMistakes = (topicId: string) =>
  db().prepare("SELECT * FROM mistakes WHERE topic_id = ? ORDER BY count DESC, updated_at DESC LIMIT 5").all(topicId) as Mistake[];
export const addMistakeManual = (topicId: string | null, text: string) =>
  db().prepare("INSERT INTO mistakes (topic_id, text, source) VALUES (?, ?, 'you')").run(topicId, text.trim());
export const updateMistakeText = (id: number, text: string) => db().prepare("UPDATE mistakes SET text = ?, updated_at = datetime('now') WHERE id = ?").run(text.trim(), id);
export const deleteMistake = (id: number) => db().prepare("DELETE FROM mistakes WHERE id = ?").run(id);

// ---------- Streak days ----------
export type Day = { date: string; exercise_passed: number; kept: number };
export const allDays = () => db().prepare("SELECT * FROM days ORDER BY date").all() as Day[];
export const getDay = (date: string) => db().prepare("SELECT * FROM days WHERE date = ?").get(date) as Day | undefined;
export function saveDay(date: string, exercisePassed: boolean, kept: boolean) {
  db().prepare(`INSERT INTO days (date, exercise_passed, kept) VALUES (?, ?, ?)
    ON CONFLICT(date) DO UPDATE SET exercise_passed = excluded.exercise_passed, kept = excluded.kept`).run(date, exercisePassed ? 1 : 0, kept ? 1 : 0);
}

// ---------- Interviews ----------
export type Interview = { id: number; kind: string; language: string | null; started_at: string; ended_at: string | null; code: string | null; feedback: string | null };
export const createInterview = (kind: string, language: string) =>
  Number(db().prepare("INSERT INTO interviews (kind, language) VALUES (?, ?)").run(kind, language).lastInsertRowid);
export const getInterview = (id: number) => db().prepare("SELECT * FROM interviews WHERE id = ?").get(id) as Interview | undefined;
export const allInterviews = () => db().prepare("SELECT * FROM interviews ORDER BY id DESC").all() as Interview[];
export const saveInterviewCode = (id: number, code: string) => db().prepare("UPDATE interviews SET code = ? WHERE id = ?").run(code, id);
export const endInterview = (id: number, feedback: string) =>
  db().prepare("UPDATE interviews SET ended_at = datetime('now'), feedback = ? WHERE id = ?").run(feedback, id);

// ---------- Project reviews ----------
export type ProjectReview = { id: number; topic_id: string; folder: string; created_at: string; passed: number; result: string };
export const addProjectReview = (topicId: string, folder: string, passed: boolean, result: string) =>
  db().prepare("INSERT INTO project_reviews (topic_id, folder, passed, result) VALUES (?, ?, ?, ?)").run(topicId, folder, passed ? 1 : 0, result);
export const projectReviews = (topicId: string) =>
  db().prepare("SELECT * FROM project_reviews WHERE topic_id = ? ORDER BY id DESC").all(topicId) as ProjectReview[];

// ---------- Sketchpad ----------
export const getSketch = (exerciseId: string) =>
  (db().prepare("SELECT scene FROM sketches WHERE exercise_id = ?").get(exerciseId) as { scene: string } | undefined)?.scene ?? null;
export const saveSketchScene = (exerciseId: string, scene: string) =>
  db().prepare(`INSERT INTO sketches (exercise_id, scene) VALUES (?, ?)
    ON CONFLICT(exercise_id) DO UPDATE SET scene = excluded.scene, updated_at = datetime('now')`).run(exerciseId, scene);
