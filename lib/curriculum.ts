// Reads the Curriculum Map from the curriculum/ folder. The markdown files are the source of truth (ADR 0001).
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import ts from "typescript";
import { LANGUAGES, LANGUAGE_IDS, type Language } from "./languages.ts";

export type { Language };

export type Exercise = {
  id: string; // "p1-03-02-shipping-cost"
  topicId: string; // "1.3"
  title: string;
  difficulty: string;
  body: string; // Problem, Examples, Constraints: what the Learner sees
  hints: string[];
  explainBack: string[];
  starter: string; // TypeScript
  test: string; // TypeScript
  // Per language, where that language's files exist. javascript is derived from typescript (types stripped).
  languages: Partial<Record<Language, { starter: string; test: string }>>;
};

export type Topic = {
  id: string; // "1.3"
  phase: number;
  number: number;
  title: string;
  learnedWhen: string;
  teach: string;
  probe: string;
  practice: string; // hands-on work outside the app (phases without in-app Exercises)
  sources: string;
  exerciseIds: string[];
};

export type Phase = { number: number; title: string };

export type Curriculum = { phases: Phase[]; topics: Topic[]; exercises: Map<string, Exercise> };

const ROOT = join(process.cwd(), "curriculum");

// Splits markdown into { heading: body } for one heading level ("## ").
export function sections(md: string, marker = "## "): Record<string, string> {
  const out: Record<string, string> = {};
  let current = "";
  for (const line of md.split(/\r?\n/)) {
    if (line.startsWith(marker)) {
      current = line.slice(marker.length).trim();
      out[current] = "";
    } else if (current) {
      out[current] += line + "\n";
    }
  }
  for (const k of Object.keys(out)) out[k] = out[k].trim();
  return out;
}

const listItems = (text: string) =>
  text.split(/\r?\n/).map((l) => l.match(/^\s*(?:\d+\.|-)\s+(.*)$/)?.[1]).filter((x): x is string => !!x);

const field = (text: string, name: string) => text.match(new RegExp(`\\*\\*${name}:\\*\\*\\s*(.*)`))?.[1]?.trim() ?? "";

export function parsePhase(md: string, phase: number): Topic[] {
  return Object.entries(sections(md))
    .map(([heading, body]) => {
      const m = heading.match(/^(\d+)\.\s+(.*)$/);
      if (!m) return null;
      const exercisesText = body.split("**Exercises:**")[1] ?? "";
      return {
        id: `${phase}.${m[1]}`,
        phase,
        number: Number(m[1]),
        title: m[2],
        learnedWhen: field(body, "Learned when"),
        teach: field(body, "Teach"),
        probe: field(body, "Probe"),
        practice: field(body, "Practice"),
        sources: field(body, "Sources"),
        exerciseIds: listItems(exercisesText)
          .map((item) => item.match(/^`([^`]+)`/)?.[1])
          .filter((x): x is string => !!x)
          .map((folder) => `p${phase}-${folder}`),
      };
    })
    .filter((t): t is Topic => t !== null);
}

// JavaScript version of a starter: types stripped, then re-indented to 2 spaces to match the .ts files.
export function stripTypes(code: string): string {
  const out = ts.transpileModule(code, { compilerOptions: { target: ts.ScriptTarget.ESNext, module: ts.ModuleKind.ESNext } }).outputText;
  const twoSpaceIndent = out.replace(/^( {4})+/gm, (m) => " ".repeat(m.length / 2));
  return twoSpaceIndent.replace(/\n{3,}/g, "\n\n").trim() + "\n";
}

export function parseExercise(md: string, id: string, topicId: string, starter: string, test: string, extra: Exercise["languages"] = {}): Exercise {
  const title = md.match(/^# (.*)$/m)?.[1]?.trim() ?? id;
  const s = sections(md);
  const body = ["Problem", "Examples", "Constraints"]
    .filter((k) => s[k])
    .map((k) => `## ${k}\n\n${s[k]}`)
    .join("\n\n");
  return {
    id,
    topicId,
    title,
    difficulty: md.match(/^Difficulty:\s*(.*)$/m)?.[1]?.trim() ?? "",
    body,
    hints: listItems(s["Hints"] ?? ""),
    explainBack: listItems(s["Explain-back"] ?? ""),
    starter,
    test,
    languages: { typescript: { starter, test }, javascript: { starter: stripTypes(starter), test }, ...extra },
  };
}

let cached: Curriculum | undefined;

// ponytail: loaded once per server process; restart `npm run dev` after editing curriculum files.
export function loadCurriculum(root = ROOT): Curriculum {
  if (cached && root === ROOT) return cached;
  const phases: Phase[] = [];
  const topics: Topic[] = [];
  const exercises = new Map<string, Exercise>();
  const phaseDirs = readdirSync(root).filter((d) => /^phase-\d+$/.test(d)).sort((a, b) => Number(a.slice(6)) - Number(b.slice(6)));
  for (const dir of phaseDirs) {
    const phase = Number(dir.slice(6));
    const phasePath = join(root, dir, "PHASE.md");
    if (!existsSync(phasePath)) continue;
    const phaseMd = readFileSync(phasePath, "utf8");
    phases.push({ number: phase, title: phaseMd.match(/^# Phase \d+\s*[—-]\s*(.*)$/m)?.[1]?.trim() ?? `Phase ${phase}` });
    for (const topic of parsePhase(phaseMd, phase)) {
      topics.push(topic);
      for (const exId of topic.exerciseIds) {
        const folder = join(root, dir, exId.slice(`p${phase}-`.length));
        const read = (f: string) => readFileSync(join(folder, f), "utf8");
        const extra: Exercise["languages"] = {};
        for (const lang of LANGUAGE_IDS) {
          const files = LANGUAGES[lang].files;
          if (lang === "typescript" || !files || !existsSync(join(folder, files.starter))) continue;
          extra[lang] = { starter: read(files.starter), test: read(files.test) };
        }
        exercises.set(exId, parseExercise(read("exercise.md"), exId, topic.id, read("starter.ts"), read("test.ts"), extra));
      }
    }
  }
  const result = { phases, topics, exercises };
  if (root === ROOT) cached = result;
  return result;
}

export function getTopic(id: string) {
  return loadCurriculum().topics.find((t) => t.id === id);
}

export function getExercise(id: string) {
  return loadCurriculum().exercises.get(id);
}
