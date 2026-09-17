// Runs an Exercise's tests against the Learner's code in a throwaway folder, in the chosen language.
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { LANGUAGES, type Language } from "./languages.ts";

export type TestRun = { passed: boolean; output: string; timedOut: boolean };

const TIMEOUT_MS = 20_000;

function runCommand(cmd: string[], cwd: string): Promise<{ code: number | null; output: string; timedOut: boolean }> {
  return new Promise((resolve) => {
    const child = spawn(cmd[0], cmd.slice(1), { cwd, env: { ...process.env, NO_COLOR: "1", FORCE_COLOR: "0", PYTHONDONTWRITEBYTECODE: "1" } });
    let output = "";
    child.stdout.on("data", (d) => (output += d));
    child.stderr.on("data", (d) => (output += d));
    const timer = setTimeout(() => child.kill(), TIMEOUT_MS);
    child.on("error", (e) => {
      clearTimeout(timer);
      resolve({ code: 1, output: `Couldn't start ${cmd[0]}: ${e.message}. Is it installed and on your PATH?`, timedOut: false });
    });
    child.on("close", (code, signal) => {
      clearTimeout(timer);
      resolve({ code, output, timedOut: signal !== null });
    });
  });
}

// ponytail: no sandbox. The code is the Learner's own, on their own machine; an infinite loop is killed by the timeout.
export async function runTests(code: string, test: string, language: Language): Promise<TestRun> {
  const spec = LANGUAGES[language];
  const dir = mkdtempSync(join(tmpdir(), "poopy-run-"));
  try {
    writeFileSync(join(dir, "package.json"), '{"type":"module"}');
    writeFileSync(join(dir, spec.solutionFile), code);
    writeFileSync(join(dir, spec.testFile), test);
    let output = "";
    for (const cmd of spec.commands) {
      const r = await runCommand(cmd, dir);
      output += r.output;
      if (r.timedOut) return { passed: false, timedOut: true, output: `Stopped after ${TIMEOUT_MS / 1000} s — is there a loop that never ends?\n\n${output}`.replaceAll(dir, ".") };
      if (r.code !== 0) return { passed: false, timedOut: false, output: output.replaceAll(dir, ".") };
    }
    return { passed: true, timedOut: false, output: output.replaceAll(dir, ".") };
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}
