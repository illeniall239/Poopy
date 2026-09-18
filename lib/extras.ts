// Extra practice: Tutor-generated exercises on a topic, verified before they're shown, stored under data/extra/.
// They never count towards a Topic being Learned; they're for digging deeper.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { getTopic, loadCurriculum, parseExercise, stripTypes, type Exercise, type Topic } from "./curriculum.ts";
import { LANGUAGES, type Language } from "./languages.ts";
import { jsonReply } from "./llm.ts";
import { runTests } from "./runner.ts";
import { topicMistakes } from "./db.ts";

const EXTRA_DIR = join(process.cwd(), "data", "extra");
export const isExtraId = (id: string) => id.startsWith("x-");

// data/extra/<topicId>/<slug>/{exercise.md, starter.<ext>, test.<ext>, reference.<ext>}
export function loadExtras(topicId?: string): Exercise[] {
  if (!existsSync(EXTRA_DIR)) return [];
  const out: Exercise[] = [];
  for (const tid of readdirSync(EXTRA_DIR)) {
    if (topicId && tid !== topicId) continue;
    for (const slug of readdirSync(join(EXTRA_DIR, tid))) {
      const folder = join(EXTRA_DIR, tid, slug);
      if (!existsSync(join(folder, "exercise.md"))) continue;
      const read = (f: string) => readFileSync(join(folder, f), "utf8");
      const langs: Exercise["languages"] = {};
      for (const [lang, spec] of Object.entries(LANGUAGES) as [Language, (typeof LANGUAGES)[Language]][]) {
        if (!spec.files || !existsSync(join(folder, spec.files.starter))) continue;
        langs[lang] = { starter: read(spec.files.starter), test: read(spec.files.test) };
      }
      const ts = langs.typescript;
      if (ts) langs.javascript = { starter: stripTypes(ts.starter), test: ts.test };
      const first = ts ?? Object.values(langs)[0];
      if (!first) continue;
      const ex = parseExercise(read("exercise.md"), `x-${tid}-${slug}`, tid, first.starter, first.test, langs);
      ex.languages = langs; // parseExercise assumes a TypeScript starter; keep only what really exists
      out.push(ex);
    }
  }
  return out;
}

export function getExtra(id: string): Exercise | undefined {
  const m = id.match(/^x-([^-]+)-(.+)$/);
  return m ? loadExtras(m[1]).find((e) => e.id === id) : undefined;
}

const schema = {
  type: "object",
  properties: {
    title: { type: "string" },
    slug: { type: "string", description: "kebab-case, letters/digits/hyphens only" },
    difficulty: { type: "integer", minimum: 1, maximum: 3 },
    problem: { type: "string", description: "Markdown. Names the function(s) exactly as in the starter." },
    examples: { type: "string", description: "Plain text lines like `f(1, 2) → 3`, no code fence" },
    constraints: { type: "string", description: "Markdown bullet list" },
    hints: { type: "array", items: { type: "string" }, minItems: 4, maxItems: 4 },
    explainBack: { type: "array", items: { type: "string" }, minItems: 3, maxItems: 4 },
    starter: { type: "string" },
    test: { type: "string" },
    reference: { type: "string" },
  },
  required: ["title", "slug", "difficulty", "problem", "examples", "constraints", "hints", "explainBack", "starter", "test", "reference"],
};

type Generated = {
  title: string; slug: string; difficulty: number; problem: string; examples: string; constraints: string;
  hints: string[]; explainBack: string[]; starter: string; test: string; reference: string;
};

function exerciseMd(g: Generated, topic: Topic) {
  return `# ${g.title}\n\nTopic: ${topic.number}. ${topic.title}\nDifficulty: ${g.difficulty} of 3\n\n## Problem\n\n${g.problem.trim()}\n\n## Examples\n\n\`\`\`\n${g.examples.trim()}\n\`\`\`\n\n## Constraints\n\n${g.constraints.trim()}\n\n## Hints\n\n${g.hints.map((h, i) => `${i + 1}. ${h.trim()}`).join("\n")}\n\n## Explain-back\n\n${g.explainBack.map((q) => `- ${q.trim()}`).join("\n")}\n`;
}

// Generates one new exercise for the topic in `language`, verifies it (reference passes, starter fails), saves it.
export async function generateExtra(topicId: string, language: Language): Promise<{ id: string; title: string }> {
  const topic = getTopic(topicId);
  if (!topic) throw new Error(`Unknown topic ${topicId}`);
  const { exercises } = loadCurriculum();
  const builtIn = topic.exerciseIds.map((id) => exercises.get(id)!);
  const wanted: Language = language === "javascript" ? "typescript" : language; // JS is derived from TS
  const offered = new Set(builtIn.flatMap((e) => Object.keys(e.languages)));
  const lang: Language = offered.size === 0 || offered.has(wanted) ? wanted : (offered.has("python") ? "python" : ([...offered][0] as Language));
  const spec = LANGUAGES[lang];
  if (!spec.files) throw new Error(`Can't generate for ${lang}`);
  const existingTitles = [...builtIn.map((e) => e.title), ...loadExtras(topicId).map((e) => e.title)];
  const exemplar = builtIn.find((e) => e.languages[lang]);
  const exemplarFiles = exemplar
    ? `\n## Format exemplar (a built-in exercise of this topic in ${spec.label}; copy its conventions exactly)\n### starter\n\`\`\`\n${exemplar.languages[lang]!.starter}\n\`\`\`\n### test\n\`\`\`\n${exemplar.languages[lang]!.test}\n\`\`\`\n`
    : "";

  const system = `You write original practice exercises for a Socratic programming tutor. Output must be valid for the JSON schema. Never reuse a known LeetCode/Exercism problem text; invent a fresh scenario. The exercise must be fully unit-testable by the given test conventions, deterministic, and solvable with only this topic's concepts and earlier ones.`;
  const ask = (extraNote: string) => `## Topic ${topic.id}: ${topic.title}
Learned when: ${topic.learnedWhen}
Concepts: ${topic.teach}
Misconceptions to target: ${topic.probe}
${topicMistakes(topicId).length ? `This Learner's own recurring mistakes on this topic (build the exercise so these get exercised):\n${topicMistakes(topicId).map((m) => `- ${m.text}`).join("\n")}\n` : ""}
## Already used titles (do not repeat these problems or close variants)
${existingTitles.map((t) => `- ${t}`).join("\n")}

## Language: ${spec.label}
Files: starter (signatures only; body throws "Not implemented" the way the exemplar does), test (5–9 tests, same framework and import style as the exemplar; the solution file is named ${spec.solutionFile}), reference (a clean correct solution with the same signatures; the first line must be the same "Reference solution" comment as built-in exercises).
${exemplarFiles}
## Requirements
- Difficulty 2 or 3 of 3: a real step up from the built-in exercises, still one function or small class.
- Problem text names the function(s) exactly as in the starter and states every tested behaviour (empty input, ordering, ties, errors).
- Hints: exactly 4 guiding questions, each more specific, none revealing the solution. Explain-back: 3–4 questions targeting the misconceptions above (and complexity when relevant).
- Tests must fail against the starter and pass against the reference.
${extraNote}`;

  const dir = join(EXTRA_DIR, topicId);
  let note = "";
  let last = "";
  for (let attempt = 0; attempt < 2; attempt++) {
    const { value: g } = await jsonReply<Generated>(system, [{ role: "user", content: ask(note) }], schema);
    const refRun = await runTests(g.reference, g.test, lang);
    const starterRun = await runTests(g.starter, g.test, lang);
    if (refRun.passed && !starterRun.passed) {
      const slug = g.slug.toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || `extra-${Date.now()}`;
      const folder = join(dir, slug);
      if (existsSync(folder)) rmSync(folder, { recursive: true, force: true });
      mkdirSync(folder, { recursive: true });
      writeFileSync(join(folder, "exercise.md"), exerciseMd(g, topic));
      writeFileSync(join(folder, spec.files.starter), g.starter.trimEnd() + "\n");
      writeFileSync(join(folder, spec.files.test), g.test.trimEnd() + "\n");
      writeFileSync(join(folder, spec.files.reference), g.reference.trimEnd() + "\n");
      return { id: `x-${topicId}-${slug}`, title: g.title };
    }
    last = refRun.passed ? "The tests passed against the starter (tests too weak or starter already solves it)." : `The reference failed its own tests:\n${refRun.output.slice(0, 1500)}`;
    note = `\n## Your previous attempt was rejected\n${last}\nFix it: the reference must pass every test and the starter must fail at least one.`;
  }
  throw new Error(`Couldn't produce a verified exercise after two attempts. ${last.slice(0, 300)}`);
}
