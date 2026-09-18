// Interview Practice: mock interviews, separate from Sessions (CONTEXT.md). The interviewer never writes the answer.
import type { ChatMessage } from "./llm.ts";
import type { Message } from "./db.ts";
import { LANGUAGES, type Language } from "./languages.ts";
import type { Topic } from "./curriculum.ts";

export type InterviewKind = "dsa" | "code" | "design" | "behavioral";

export const INTERVIEW_KINDS: Record<InterviewKind, { label: string; minutes: number; blurb: string; editor: boolean }> = {
  dsa: { label: "Coding (timed DSA)", minutes: 45, editor: true, blurb: "One problem, 45 minutes. Think out loud, code in the editor, then analyse complexity." },
  code: { label: "Explain this code", minutes: 20, editor: false, blurb: "The interviewer shows a snippet. Explain what it does, find what's wrong, and improve it." },
  design: { label: "System design", minutes: 45, editor: false, blurb: "Design a small real system: requirements, API, data model, components, scaling." },
  behavioral: { label: "Behavioral", minutes: 30, editor: false, blurb: "\"Tell me about a time…\" questions. Answer with specific stories (situation, task, action, result)." },
};

export const isInterviewKind = (k: string): k is InterviewKind => k in INTERVIEW_KINDS;

const INTERVIEWER = `You are a realistic, fair technical interviewer at a product company, interviewing a junior full-stack developer candidate. Stay in character for the whole interview.

Rules:
- Never give the solution, never write the candidate's code, never answer your own questions.
- Keep each turn short (usually 1–4 sentences), like a real interviewer speaking.
- Ask one question at a time. Probe vague answers ("what do you mean by…", "what happens if…").
- If the candidate is stuck for a while, give one small nudge, the kind a real interviewer would give, and note to yourself that they needed it.
- Be warm but honest; don't praise things that aren't good.
- When the interview has covered what it should, tell the candidate they can press **End interview** for feedback.`;

const PER_KIND: Record<InterviewKind, (language: Language) => string> = {
  dsa: (language) => `This is a coding interview (about 45 minutes). The candidate codes in ${LANGUAGES[language].label} in an editor you can see; their current code is included with each message.
Open by presenting ONE original problem of medium interview difficulty (a common pattern: hashing, two pointers, sliding window, stack, binary search, trees, graphs, heaps, backtracking or DP — pick any; do not copy LeetCode text). Give the function signature in ${LANGUAGES[language].label}, one or two examples, and constraints. Then:
1. Let them ask clarifying questions and state an approach before coding (push for this if they jump straight to code).
2. While they code, react to what you see only when asked or when they're clearly heading into a wall.
3. When they say they're done, ask them to walk through an example by hand, then ask time and space complexity, then one follow-up variation.`,
  code: (language) => `This is an "explain this code" interview (about 20 minutes). Open by showing ONE realistic ${LANGUAGES[language].label} snippet of 15–40 lines in a fenced code block — the kind found in a real web codebase (data transformation, a small class, an async helper, a React-less utility). Include one subtle bug or design problem, but don't say so. Ask them to explain what it does. Then, one at a time: what it returns for a specific input you choose, the bug or edge case, its complexity, and how they'd improve it.`,
  design: () => `This is a system design interview for a junior candidate (about 45 minutes). Open by giving ONE classic but small design prompt (e.g. a URL shortener, a rate limiter, a notification service, a paste bin, a chat for a small team — choose one) in two sentences. Drive the conversation through: clarifying requirements and scale estimates → API endpoints → data model → high-level components → one bottleneck and how to scale it → one failure mode. Expect junior-level depth, but ask them to justify every choice.`,
  behavioral: () => `This is a behavioral interview (about 30 minutes). Ask 3–4 questions of the "tell me about a time…" kind, suited to someone early in their career (learning something hard, a mistake they made, disagreeing with someone, a project they're proud of, working under a deadline). For each answer, ask follow-ups until you have the situation, their own actions (not the team's), and a concrete result. If an answer is vague or hypothetical ("I would…"), ask for a real example.`,
};

const toChat = (history: Message[]): ChatMessage[] =>
  history.map((m) => ({ role: m.role === "learner" ? "user" : "assistant", content: m.content }));

export function interviewPrompt(kind: InterviewKind, language: Language, history: Message[], code: string | null) {
  const context = `${PER_KIND[kind](language)}${kind === "dsa" && code ? `\n\n## The candidate's current code\n\`\`\`\n${code}\n\`\`\`` : ""}${history.length ? "" : "\n\nBegin the interview now: greet the candidate in one sentence and give the first prompt."}`;
  return { system: INTERVIEWER, messages: [{ role: "user" as const, content: context }, ...toChat(history)] };
}

export const feedbackSchema = {
  type: "object",
  properties: {
    rating: { type: "string", enum: ["strong hire", "hire", "lean no hire", "no hire"] },
    summary: { type: "string" },
    strengths: { type: "array", items: { type: "string" } },
    improvements: { type: "array", items: { type: "string" } },
    mistakes: {
      type: "array",
      items: { type: "object", properties: { topicId: { type: ["string", "null"] }, text: { type: "string" } }, required: ["topicId", "text"] },
    },
  },
  required: ["rating", "summary", "strengths", "improvements", "mistakes"],
};

export type Feedback = { rating: string; summary: string; strengths: string[]; improvements: string[]; mistakes: { topicId: string | null; text: string }[] };

export function feedbackPrompt(kind: InterviewKind, history: Message[], code: string | null, topics: Topic[]) {
  const transcript = history.map((m) => `${m.role === "learner" ? "Candidate" : "Interviewer"}: ${m.content}`).join("\n\n");
  return {
    system: `You write interview feedback for a junior developer candidate, as a calibrated hiring-panel interviewer would: specific, evidence-based, kind and honest. Rate against a junior full-stack bar. Quote or reference what the candidate actually said or wrote. Never include a full solution.`,
    messages: [{
      role: "user" as const,
      content: `Interview type: ${INTERVIEW_KINDS[kind].label}

## Transcript
${transcript || "(the candidate said nothing)"}
${kind === "dsa" ? `\n## Final code\n\`\`\`\n${code ?? "(none)"}\n\`\`\`` : ""}

## Curriculum topics (for tagging mistakes)
${topics.map((t) => `${t.id} ${t.title}`).join("\n")}

Write: a rating; a 3–5 sentence summary addressed to the candidate; 2–4 strengths; 2–4 concrete improvements (what to practise next). List the specific mistakes or misconceptions shown (e.g. "forgot to handle the empty input", "said a hash map lookup is O(n)"), each tagged with the most relevant topic id from the list, or null if none fits. If the candidate barely participated, say so and rate "no hire".`,
    }],
  };
}
