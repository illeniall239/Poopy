// Proves every Exercise's tests are meaningful, in every language it has files for:
// they pass against the reference and fail against the starter.
// Usage: node scripts/verify-exercises.mjs [path-filter] [--lang python,java]
import { readdirSync, existsSync, mkdtempSync, copyFileSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";

const root = new URL("../curriculum", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const args = process.argv.slice(2);
const langArg = args.indexOf("--lang");
const onlyLangs = langArg >= 0 ? args[langArg + 1].split(",") : null;
const filter = args.filter((a, i) => a !== "--lang" && (langArg < 0 || i !== langArg + 1))[0] ?? "";

// Mirrors lib/languages.ts (kept separate so this script stays plain Node).
const LANGS = {
  typescript: { starter: "starter.ts", test: "test.ts", reference: "reference.ts", solution: "solution.ts", testFile: "test.ts",
    commands: [[process.execPath, "--experimental-strip-types", "--no-warnings", "--test", "--test-timeout=5000", "test.ts"]] },
  python: { starter: "starter.py", test: "test.py", reference: "reference.py", solution: "solution.py", testFile: "test.py",
    commands: [["python", "-X", "utf8", "test.py"]] },
  java: { starter: "starter.java", test: "test.java", reference: "reference.java", solution: "Solution.java", testFile: "SolutionTest.java",
    commands: [["javac", "-encoding", "UTF-8", "Solution.java", "SolutionTest.java"], ["java", "-Dfile.encoding=UTF-8", "-cp", ".", "SolutionTest"]] },
};

function exerciseDirs(dir) {
  return readdirSync(dir, { withFileTypes: true }).filter((e) => e.isDirectory()).flatMap((e) => {
    const p = join(dir, e.name);
    return existsSync(join(p, "exercise.md")) ? [p] : exerciseDirs(p);
  });
}

function run(dir, lang, solutionSource) {
  const L = LANGS[lang];
  const tmp = mkdtempSync(join(tmpdir(), "ex-"));
  try {
    writeFileSync(join(tmp, "package.json"), '{"type":"module"}');
    copyFileSync(join(dir, L.test), join(tmp, L.testFile));
    copyFileSync(join(dir, solutionSource), join(tmp, L.solution));
    let out = "";
    for (const cmd of L.commands) {
      const r = spawnSync(cmd[0], cmd.slice(1), { cwd: tmp, encoding: "utf8", timeout: 120000, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" } });
      out += (r.stdout ?? "") + (r.stderr ?? "");
      if (r.status !== 0) return { ok: false, out };
    }
    return { ok: true, out };
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

let failures = 0, checked = 0;
const noLanguage = (dir) => !Object.values(LANGS).some((L) => existsSync(join(dir, L.starter)));
const dirs = exerciseDirs(root).filter((d) => d.includes(filter));
for (const dir of dirs) {
  const name = dir.slice(root.length + 1);
  if (noLanguage(dir)) { failures++; console.log(`FAIL ${name}: no starter in any language`); continue; }
  for (const [lang, L] of Object.entries(LANGS)) {
    if (onlyLangs && !onlyLangs.includes(lang)) continue;
    const present = [L.starter, L.test, L.reference].filter((f) => existsSync(join(dir, f)));
    if (present.length === 0) continue;
    if (present.length < 3) { failures++; console.log(`FAIL ${name} [${lang}]: has ${present.join(", ")} but not all of ${L.starter}, ${L.test}, ${L.reference}`); continue; }
    if (!existsSync(join(dir, "exercise.md"))) { failures++; console.log(`FAIL ${name}: missing exercise.md`); continue; }
    checked++;
    const ref = run(dir, lang, L.reference);
    const starter = run(dir, lang, L.starter);
    if (!ref.ok) { failures++; console.log(`FAIL ${name} [${lang}]: tests fail against reference\n${ref.out.slice(0, 1500)}`); }
    else if (starter.ok) { failures++; console.log(`FAIL ${name} [${lang}]: tests pass against starter (tests too weak)`); }
    else console.log(`ok   ${name} [${lang}]`);
  }
}
console.log(`\n${checked - failures}/${checked} exercise-language pairs verified across ${dirs.length} exercises`);
process.exit(failures ? 1 : 0);
