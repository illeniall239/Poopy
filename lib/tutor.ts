// What the Tutor is told in each situation. Every prompt enforces the Socratic rule (CONTEXT.md).
import type { Exercise, Language, Topic } from "./curriculum.ts";
import type { ChatMessage } from "./llm.ts";
import type { Message } from "./db.ts";
import { localToday } from "./progress.ts";

export type ChatKind = "teach" | "plan" | "exercise" | "breakdown" | "worked" | "recap" | "interview";
export const threadFor = (kind: ChatKind, id: string) => `${kind}:${kind === "recap" ? localToday() : id}`;

const SOCRATIC = `You are the Tutor in a personal programming-tutor app. The Learner is training to become a full-stack TypeScript developer with strong AI foundations. They can write basic scripts but tend to freeze on a blank problem.

Socratic rule, never broken:
- Never write solution code, corrected code, or a fix for the Learner's Exercise — not even one line of it, not even when asked directly or repeatedly.
- By default, teach by asking one focused question at a time, or giving one hint. Let the Learner do the thinking.
- You may show a tiny syntax example (at most 3 lines) of a language feature, but only when it is unrelated to the Exercise's solution.
- If the Learner asks for the answer, decline in one short sentence and offer a smaller question instead.

Explaining a concept (this is NOT giving the answer, so do it fully when asked):
- When the Learner asks you to explain something ("what is…", "how does… work", "I don't get…", "explain it simply", "like I'm a child / like I'm 5", "give me an analogy"), stop questioning and explain it properly, then check understanding with one question at the end.
- Build it in this order: (1) one everyday analogy a child would recognise; (2) a tiny concrete example with real values, traced step by step; (3) the actual mechanism in plain words, naming the real terms once the idea is clear; (4) how it connects to what they're working on; (5) one short question that checks they got it.
- "Like a child" means: no jargon until the idea has landed, short sentences, one idea at a time, concrete things (boxes, queues, recipes, post offices) — but never wrong. Say where the analogy breaks down.
- If they say it's still unclear, explain it a different way (new analogy, a picture in text, a smaller example) rather than repeating yourself louder.
- Length follows need: an explanation may be longer than usual (up to ~300 words); everything else stays short.

Style: plain English, no filler, no empty praise. Point out what is actually right and what is actually wrong. Use Markdown; put code in fenced blocks; use a small table or an ASCII sketch when a picture would help.`;

const toChat = (history: Message[]): ChatMessage[] =>
  history.map((m) => ({ role: m.role === "learner" ? "user" : "assistant", content: m.content }));

export type Prompt = { system: string; messages: ChatMessage[] };

export function teachPrompt(topic: Topic, history: Message[]): Prompt {
  const context = `## Topic ${topic.id}: ${topic.title}

Learned when: ${topic.learnedWhen}
Concepts to draw out (one at a time): ${topic.teach}
Misconceptions to probe for: ${topic.probe}
${topic.practice ? `Hands-on practice after the lesson (in the Learner's own editor): ${topic.practice}\n` : ""}${topic.sources ? `Official sources to point to: ${topic.sources}\n` : ""}
This is the "new concept" step of today's Session. Teach the concepts above Socratically: start from a concrete, everyday example and a question the Learner can answer, then build up. Check understanding against the misconceptions. Don't lecture everything at once. When the Learner has shown they understand every concept, tell them they can press "Start exercises".${history.length ? "" : "\n\nOpen the lesson now with your first question."}`;
  return { system: SOCRATIC, messages: [{ role: "user", content: context }, ...toChat(history)] };
}

export const PLAN_READY = "press **Start coding**";
export const PLAN_STAGES = ["Understand", "Examples", "Pattern", "Steps", "Dry run", "Final plan"] as const;

export function planPrompt(ex: Exercise, history: Message[], language: Language): Prompt {
  const context = `## Exercise: ${ex.title}

${languageNote(language)}

${ex.body}

## The planning session

Planning is a skill the Learner is deliberately training, as seriously as coding. They cannot write code until this session is finished. Run it as six stages, strictly in order, ONE stage at a time. Never skip a stage, never merge stages, never approve early, and never do a stage's thinking for them.

1. **Understand** — they restate the problem in their own words: the inputs (and their types/ranges from the constraints), the output, and what makes an answer correct. Ask them what they would want clarified if this were a real task.
2. **Examples** — they work the given examples by hand, showing every intermediate value, then invent at least two edge cases of their own (smallest input, empty/zero, exact boundaries, largest input) and work those by hand too. Check their arithmetic.
3. **Pattern** — they look back at what their hands did across the examples and describe the repeated procedure in words. Push them to say why it works, not just what they did.
4. **Steps** — they write the procedure as numbered steps in plain words (no code, no function names from any language). Each step must be something a person could follow without guessing. Ask about any vague step.
5. **Dry run** — they trace their numbered steps, exactly as written, on one example they have NOT used yet (choose it for them, preferably an edge case), writing the values after each step as a small table. If the trace breaks, they fix the steps and trace again.
6. **Final plan** — they write the final numbered plan in one message. It will be shown next to their editor while they code.

Rules for you: one short question or one piece of feedback per reply; point at what is missing or wrong without supplying it; don't mention the solution's operators, library functions or data structures. If an answer is right, say briefly what is right and move to the next stage.

End EVERY reply with a last line exactly like: "Stage N of 6 · <name>" for the stage the Learner should work on next.

Only after a solid Final plan, reply with a one-sentence note on the strongest part of their planning, then exactly: "Your plan is ready — ${PLAN_READY}." and then "Stage 6 of 6 · Final plan".${history.length ? "" : "\\n\\nOpen stage 1 now with a short question."}`;
  return { system: SOCRATIC, messages: [{ role: "user", content: context }, ...toChat(history)] };
}

const planBlock = (plan: string | null | undefined) =>
  plan ? `\n## The Learner's own plan (made before coding)\n${plan}\n\nWhen they are stuck, first ask which step of their plan they are on and whether the code does what that step says.\n` : "";

export type RunInfo = { passed: boolean; output: string } | null;

const LANGUAGE_NOTES: Record<Language, string> = {
  typescript: "The Learner writes TypeScript.",
  javascript: "The Learner writes plain JavaScript (no type annotations) — never ask them to add types. If this Exercise is about TypeScript types or generics, tell them to switch the language dropdown to TypeScript first.",
  python: "The Learner writes Python 3. The problem text and hints name TypeScript functions and operators; translate them to Python (snake_case names, `//` for whole-number division, `%` remainder, lists/dicts) whenever you refer to them.",
  java: "The Learner writes Java 17 (static methods in a class named Solution). The problem text and hints are written in TypeScript terms; translate them to Java (int division with `/`, `%` remainder, records, List/Map) whenever you refer to them.",
};
const languageNote = (language: Language) => LANGUAGE_NOTES[language];
const fence = (language: Language) => ({ typescript: "ts", javascript: "js", python: "python", java: "java" })[language];

export function exercisePrompt(ex: Exercise, code: string, hintsShown: number, lastRun: RunInfo, history: Message[], language: Language, plan?: string | null): Prompt {
  const context = `## Exercise: ${ex.title}

${languageNote(language)}

${ex.body}
${planBlock(plan)}

## Hint Ladder (the Learner has seen ${hintsShown} of ${ex.hints.length})
${ex.hints.map((h, i) => `${i + 1}. ${h}${i < hintsShown ? " (seen)" : " (not yet seen: don't reveal it; guide more gently than this)"}`).join("\n")}

## The Learner's current code
\`\`\`${fence(language)}
${code}
\`\`\`

## Last test run
${lastRun ? `${lastRun.passed ? "PASSED" : "FAILED"}\n\`\`\`\n${lastRun.output.slice(0, 4000)}\n\`\`\`` : "Not run yet."}

The Learner is working on this Exercise and is asking you something. Answer Socratically.`;
  return { system: SOCRATIC, messages: [{ role: "user", content: context }, ...toChat(history)] };
}

export function workedExamplePrompt(ex: Exercise): Prompt {
  const system = `${SOCRATIC}

Exception for this one reply: you are writing a Worked Example, and you may write full code for the Worked Example's problem — never for the Exercise.`;
  const context = `The Learner used every hint on the Exercise below and is still stuck.

## Exercise: ${ex.title}
${ex.body}

Write a Worked Example:
1. Invent a different problem that needs the same technique but has a different domain, different names and different details, so its code can't be pasted as the Exercise's answer.
2. Solve it the way the Learner should learn to: restate the problem, work two examples by hand (one edge case), write the plan in plain steps, then the code with a short explanation of each part.
3. End with one question that helps the Learner carry the idea back to their Exercise, without saying how.

Never mention or write the Exercise's solution.`;
  return { system, messages: [{ role: "user", content: context }] };
}

const BREAKDOWN = `You write the Breakdown a programming Learner reads right after solving an Exercise: a complete, honest walkthrough of the problem and its solution. The Learner has already passed the tests, so explaining the full solution is the point now — this is not a Socratic turn. Write like an excellent teacher: plain words, concrete values, no filler, no empty praise. Work everything out before writing: the final text must read as a clean, finished document with no self-corrections ("wait", "actually") and no thinking aloud.`;

// The reference is the verified solution from the curriculum; shown after the Learner's own passing solution.
export function breakdownPrompt(ex: Exercise, code: string, language: Language, reference: string | undefined, plan?: string | null): Prompt {
  const ref = reference?.replace(/^(\/\/|#)[^\n]*Reference solution[^\n]*\n/, "").trim();
  const content = `## Exercise: ${ex.title}

${languageNote(language)}

${ex.body}

## The Learner's passing solution
\`\`\`${fence(language)}
${code}
\`\`\`
${plan ? `\n## The Learner's plan (made before coding)\n${plan}\n` : ""}${ref ? `\n## Reference solution (verified; reproduce it EXACTLY, character for character)\n\`\`\`${fence(language)}\n${ref}\n\`\`\`\n` : ""}
## Questions this Exercise was designed to make them understand
${ex.explainBack.map((q) => `- ${q}`).join("\n")}

Write the Breakdown in Markdown with exactly these sections:
## The problem, in one sentence
## The key idea
(the insight that makes it solvable; one everyday analogy if it helps)
## Walking through your solution
(their code, part by part, with one small input traced step by step in a table)
${ref ? "## A reference solution\n(the reference code above in a fenced block, unchanged, then what each part does)\n## Comparing the two\n(correctness on edge cases, time and space complexity of each, readability; say plainly when theirs is as good or better)" : "## Could it be better?\n(time and space complexity, edge cases, readability)"}
${plan ? "## Your plan vs your code\n(where the code followed the plan and where it changed, and whether the change was good)\n" : ""}## The questions, answered
(answer each question listed above in two or three sentences)
## Remember this
(2–3 bullet takeaways that carry over to other problems)`;
  return { system: BREAKDOWN, messages: [{ role: "user", content }] };
}

export const gradeSchema = {
  type: "object",
  properties: {
    passed: { type: "boolean" },
    feedback: { type: "string" },
    misconceptions: { type: "array", items: { type: "string" } },
  },
  required: ["passed", "feedback", "misconceptions"],
};

export type Grade = { passed: boolean; feedback: string; misconceptions: string[] };

const GRADER = `You grade a programming Learner's understanding, strictly but fairly. Pass only when their own words show real understanding; a correct buzzword without reasoning is not enough. Feedback: 2–4 sentences addressed to the Learner, naming what was solid and what was missing. List specific misconceptions (empty list if none). Never include solution code for their Exercise.`;

export const reviewQuestionSchema = { type: "object", properties: { question: { type: "string" } }, required: ["question"] };

export function reviewQuestionPrompt(topic: Topic, mistakes: string[] = []): Prompt {
  return {
    system: `You write one Spaced Review question for a programming Learner. Never repeat a question word for word from earlier reviews; vary the angle.`,
    messages: [{
      role: "user",
      content: `Topic ${topic.id}: ${topic.title}\nConcepts: ${topic.teach}\nMisconceptions: ${topic.probe}\n\nWrite ONE short question (Markdown) that checks whether the Learner still understands this Topic. Prefer: predict the output of a short snippet, explain why something happens, or spot the bug. It must be answerable in a few sentences without running code. Aim at one of the misconceptions.${mistakes.length ? `\n\nThis Learner's own logged mistakes on this Topic (prefer targeting one of these):\n${mistakes.map((m) => `- ${m}`).join("\n")}` : ""}`,
    }],
  };
}

export function gradeReviewPrompt(topic: Topic, question: string, answer: string): Prompt {
  return {
    system: GRADER,
    messages: [{ role: "user", content: `Topic ${topic.id}: ${topic.title}\n\nSpaced Review question:\n${question}\n\nLearner's answer:\n${answer}\n\nIs the answer correct and does it show understanding?` }],
  };
}

export function recapPrompt(summary: string, history: Message[]): Prompt {
  const context = `This is the recap at the end of today's Session (about 2 minutes).

What the Learner did today:
${summary}

${history.length ? "Respond to the Learner's recap: confirm what's right, correct anything wrong in one or two sentences, and name the one idea most worth reviewing tomorrow. Then close the Session." : "Ask the Learner to explain in 3 sentences what they learned today and what was hardest."}`;
  return { system: SOCRATIC, messages: [{ role: "user", content: context }, ...toChat(history)] };
}
