import { getSetting } from "./db.ts";

// Every language an Exercise can be written in. Adding one = a row here + per-exercise files in curriculum/.
export type Language = "typescript" | "javascript" | "python" | "java";

export type LanguageSpec = {
  label: string;
  monaco: string; // Monaco language id
  editorFile: string; // file name shown in the editor
  files: { starter: string; test: string; reference: string } | null; // in the exercise folder; null = derived from typescript
  // How the runner lays out and runs a temp folder: [solution file name, test file name], then commands in order.
  solutionFile: string;
  testFile: string;
  commands: string[][];
  note: string; // shown under the editor
};

export const LANGUAGES: Record<Language, LanguageSpec> = {
  typescript: {
    label: "TypeScript",
    monaco: "typescript",
    editorFile: "solution.ts",
    files: { starter: "starter.ts", test: "test.ts", reference: "reference.ts" },
    solutionFile: "solution.ts",
    testFile: "test.ts",
    commands: [[process.execPath, "--experimental-strip-types", "--no-warnings", "--test", "--test-reporter=spec", "--test-timeout=5000", "test.ts"]],
    note: "`export` makes your function visible to the tests. Replace the `throw` line with your own code. The `: number` parts say what type each value is; Topic 1.2 explains them.",
  },
  javascript: {
    label: "JavaScript",
    monaco: "javascript",
    editorFile: "solution.js",
    files: null,
    solutionFile: "solution.ts", // plain JS is valid input for Node's type stripping, and test.ts imports ./solution.ts
    testFile: "test.ts",
    commands: [[process.execPath, "--experimental-strip-types", "--no-warnings", "--test", "--test-reporter=spec", "--test-timeout=5000", "test.ts"]],
    note: "`export` makes your function visible to the tests. Replace the `throw` line with your own code.",
  },
  python: {
    label: "Python",
    monaco: "python",
    editorFile: "solution.py",
    files: { starter: "starter.py", test: "test.py", reference: "reference.py" },
    solutionFile: "solution.py",
    testFile: "test.py",
    commands: [["python", "-X", "utf8", "test.py"]],
    note: "Replace the `raise NotImplementedError` line with your own code. Function names in the problem text are the TypeScript ones; use the snake_case names from the starter.",
  },
  java: {
    label: "Java",
    monaco: "java",
    editorFile: "Solution.java",
    files: { starter: "starter.java", test: "test.java", reference: "reference.java" },
    solutionFile: "Solution.java",
    testFile: "SolutionTest.java",
    commands: [["javac", "-encoding", "UTF-8", "Solution.java", "SolutionTest.java"], ["java", "-Dfile.encoding=UTF-8", "-cp", ".", "SolutionTest"]],
    note: "Keep the class named `Solution` and the methods `static`. Replace the `throw` line with your own code.",
  },
};

// The chosen language, or TypeScript when this Exercise has no files for it.
export function currentLanguage(ex: { languages: Partial<Record<Language, unknown>> }): Language {
  const chosen = getSetting("language", "typescript");
  if (isLanguage(chosen) && ex.languages[chosen]) return chosen;
  return ex.languages.typescript ? "typescript" : (Object.keys(ex.languages)[0] as Language);
}

export const LANGUAGE_IDS = Object.keys(LANGUAGES) as Language[];
export const isLanguage = (x: string): x is Language => x in LANGUAGES;
