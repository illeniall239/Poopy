// Project Review: the Tutor reads the Learner's own project folder (Phases 3+ practice and Portfolio Projects).
// Only source and config files are read; secrets, dependencies, builds and binaries are skipped.
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { isAbsolute, join, relative } from "node:path";
import type { Topic } from "./curriculum.ts";

const SKIP_DIRS = new Set(["node_modules", ".git", ".next", "dist", "build", "out", "coverage", ".venv", "venv", "env", "__pycache__", ".turbo", "target", ".idea", ".vscode", ".cache", ".pytest_cache", ".mypy_cache", "vendor", "data"]);
const SKIP_FILES = /^(\.env(?!\.example$).*|.*\.(pem|key|p12|pfx|crt|sqlite|sqlite3|db)|id_rsa.*|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|uv\.lock|poetry\.lock|bun\.lockb?|next-env\.d\.ts)$/i;
const TEXT_EXT = /\.(ts|tsx|js|jsx|mjs|cjs|py|java|json|ya?ml|toml|md|sql|css|scss|html|prisma|graphql|sh|ps1|txt|cfg|ini|conf)$|^(Dockerfile|Makefile|Procfile|\.env\.example|\.gitignore|\.dockerignore)$/i;
const MAX_FILE = 60_000;
const BUDGET = 140_000;

// Values that look like credentials are masked before anything leaves the machine.
const redact = (text: string) =>
  text.replace(/((?:api[_-]?key|secret|password|passwd|token|private[_-]?key|access[_-]?key)\w*\s*[:=]\s*)(["'`]?)[^\s"'`]{8,}\2/gi, "$1$2[REDACTED]$2");

export type Collected = { files: { path: string; content: string }[]; omitted: string[]; total: number };

export function collectProject(folder: string): Collected {
  if (!isAbsolute(folder)) throw new Error("Use the full path to the project folder, e.g. C:\\Users\\you\\projects\\my-api");
  if (!existsSync(folder) || !statSync(folder).isDirectory()) throw new Error(`No folder found at ${folder}`);

  const found: { path: string; size: number }[] = [];
  const walk = (dir: string) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!SKIP_DIRS.has(entry.name)) walk(full);
      } else if (entry.isFile() && TEXT_EXT.test(entry.name) && !SKIP_FILES.test(entry.name)) {
        found.push({ path: full, size: statSync(full).size });
      }
    }
  };
  walk(folder);
  if (found.length === 0) throw new Error("No source files found in that folder.");

  // README and manifests first, then the rest by path, so the reviewer sees the project's intent before its details.
  const rank = (p: string) => (/readme/i.test(p) ? 0 : /(package\.json|pyproject\.toml|docker-compose|Dockerfile|tsconfig)/i.test(p) ? 1 : 2);
  found.sort((a, b) => rank(a.path) - rank(b.path) || a.path.localeCompare(b.path));

  const files: Collected["files"] = [];
  const omitted: string[] = [];
  let total = 0;
  for (const f of found) {
    const rel = relative(folder, f.path).replaceAll("\\", "/");
    if (f.size > MAX_FILE || total + f.size > BUDGET) {
      omitted.push(rel);
      continue;
    }
    const content = redact(readFileSync(f.path, "utf8"));
    files.push({ path: rel, content });
    total += content.length;
  }
  return { files, omitted, total };
}

export const reviewSchema = {
  type: "object",
  properties: {
    passed: { type: "boolean" },
    summary: { type: "string" },
    strengths: { type: "array", items: { type: "string" } },
    issues: { type: "array", items: { type: "object", properties: { file: { type: "string" }, note: { type: "string" } }, required: ["file", "note"] } },
    questions: { type: "array", items: { type: "string" } },
    misconceptions: { type: "array", items: { type: "string" } },
  },
  required: ["passed", "summary", "strengths", "issues", "questions", "misconceptions"],
};

export type ReviewResult = { passed: boolean; summary: string; strengths: string[]; issues: { file: string; note: string }[]; questions: string[]; misconceptions: string[] };

export function reviewPrompt(topic: Topic, project: Collected) {
  return {
    system: `You review a junior developer's own practice project the way a senior engineer mentors: specific, honest, never condescending. Socratic rule: never write fixed or replacement code, never paste a solution; point at the file and the problem, and ask the question that leads them to the fix. Judge only against the practice task and the "learned when" bar below, not against production perfection.`,
    messages: [{
      role: "user" as const,
      content: `## Topic ${topic.id}: ${topic.title}
Learned when: ${topic.learnedWhen}
Practice task: ${topic.practice}
Concepts: ${topic.teach}
Misconceptions to look for: ${topic.probe}

## The project (${project.files.length} files${project.omitted.length ? `; not included because of size: ${project.omitted.join(", ")}` : ""})
${project.files.map((f) => `### ${f.path}\n\`\`\`\n${f.content}\n\`\`\``).join("\n\n")}

Decide whether this project shows the practice task done to the "learned when" bar (passed). Then: a 2–4 sentence summary to the Learner; 1–4 strengths; issues as {file, note} (the most important first, at most 8; security and correctness before style); 2–4 Socratic questions they should answer for themselves; and the specific misconceptions the code reveals (empty if none). If the folder clearly isn't this task's work, fail it and say what's missing.`,
    }],
  };
}
