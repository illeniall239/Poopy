import { test } from "node:test";
import assert from "node:assert/strict";
import { join } from "node:path";
import { loadCurriculum, parsePhase } from "./curriculum.ts";

test("parses topic fields and exercise ids", () => {
  const md = `# Phase 1\n\n## 3. Conditionals\n\n**Learned when:** orders conditions.\n\n**Teach:** if/else.\n\n**Probe:** truthiness.\n\n**Exercises:**\n- \`03-01-leap-year\` — leap years.\n- \`03-02-shipping\` — tiers.\n`;
  const [t] = parsePhase(md, 1);
  assert.equal(t.id, "1.3");
  assert.equal(t.title, "Conditionals");
  assert.equal(t.learnedWhen, "orders conditions.");
  assert.equal(t.probe, "truthiness.");
  assert.deepEqual(t.exerciseIds, ["p1-03-01-leap-year", "p1-03-02-shipping"]);
});

test("loads the real curriculum: Phase 1 topics have 3 exercises; every exercise has 4 hints and explain-back questions", () => {
  const { topics, exercises } = loadCurriculum(join(import.meta.dirname, "..", "curriculum"));
  const phase1 = topics.filter((t) => t.phase === 1);
  assert.equal(phase1.length, 15);
  for (const t of phase1) assert.equal(t.exerciseIds.length, 3, t.id);
  assert.ok(exercises.size >= 45);
  for (const ex of exercises.values()) {
    assert.equal(ex.hints.length, 4, ex.id);
    assert.ok(ex.explainBack.length >= 3, ex.id);
    assert.match(ex.body, /## Problem/, ex.id);
    assert.doesNotMatch(ex.body, /## Hints/, ex.id);
  }
});
