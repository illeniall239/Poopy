// Streams a Tutor reply as NDJSON lines: {provider} | {notice} | {text} ... then {done} or {error}.
import { getExercise, getTopic } from "@/lib/curriculum.ts";
import { addMessage, getExerciseState, getInterview, getMessages, saveExerciseState, saveInterviewCode } from "@/lib/db.ts";
import { interviewPrompt, isInterviewKind } from "@/lib/interview.ts";
import { isLanguage } from "@/lib/languages.ts";
import { streamReply } from "@/lib/llm.ts";
import { breakdownPrompt, exercisePrompt, planPrompt, recapPrompt, teachPrompt, threadFor, workedExamplePrompt, type ChatKind, type Prompt, type RunInfo } from "@/lib/tutor.ts";
import { todaySummary } from "@/app/actions.ts";
import { currentLanguage } from "@/lib/languages.ts";

type Body = { kind: ChatKind; id: string; message?: string; code?: string; lastRun?: RunInfo };

async function buildPrompt(body: Body, thread: string): Promise<Prompt> {
  const history = getMessages(thread);
  if (body.kind === "teach") {
    const topic = getTopic(body.id);
    if (!topic) throw new Error("Unknown topic");
    return teachPrompt(topic, history);
  }
  if (body.kind === "recap") return recapPrompt(await todaySummary(), history);
  if (body.kind === "interview") {
    const iv = getInterview(Number(body.id));
    if (!iv || !isInterviewKind(iv.kind)) throw new Error("Unknown interview");
    if (iv.ended_at) throw new Error("This interview has ended.");
    if (body.code !== undefined) saveInterviewCode(iv.id, body.code);
    return interviewPrompt(iv.kind, iv.language && isLanguage(iv.language) ? iv.language : "typescript", history, body.code ?? iv.code);
  }

  const ex = getExercise(body.id);
  if (!ex) throw new Error("Unknown exercise");
  const state = getExerciseState(ex.id);
  const language = currentLanguage(ex);
  if (body.kind === "plan") return planPrompt(ex, history, language);
  if (body.kind === "exercise") {
    return exercisePrompt(ex, body.code ?? state?.code ?? ex.languages[language]!.starter, state?.hints_shown ?? 0, body.lastRun ?? null, history, language, state?.plan_text);
  }
  if (body.kind === "breakdown") {
    if (!state?.tests_passed_at || !state.code) throw new Error("Pass the tests to unlock the Breakdown.");
    return breakdownPrompt(ex, state.code, language, ex.languages[language]?.reference, state.plan_text);
  }
  // worked
  if (!state || state.hints_shown < ex.hints.length) throw new Error("Use all the hints before asking for a Worked Example.");
  saveExerciseState({ ...state, worked_example: 1 });
  return workedExamplePrompt(ex);
}

export async function POST(request: Request) {
  const body = (await request.json()) as Body;
  const thread = threadFor(body.kind, body.id);
  const message = body.message?.trim();

  const encoder = new TextEncoder();
  const line = (obj: object) => encoder.encode(JSON.stringify(obj) + "\n");

  const stream = new ReadableStream({
    async start(controller) {
      try {
        if (body.kind === "worked" || body.kind === "breakdown") {
          const existing = getMessages(thread).find((m) => m.role === "tutor");
          if (existing) {
            controller.enqueue(line({ provider: existing.provider }));
            controller.enqueue(line({ text: existing.content }));
            controller.enqueue(line({ done: true }));
            return controller.close();
          }
        }
        const prompt = await buildPrompt(body, thread);
        if (message) {
          addMessage(thread, "learner", message);
          prompt.messages.push({ role: "user", content: message });
        }
        let text = "";
        let provider: string | null = null;
        for await (const chunk of streamReply(prompt.system, prompt.messages)) {
          if ("provider" in chunk) provider = chunk.provider;
          if ("text" in chunk) text += chunk.text;
          controller.enqueue(line(chunk));
        }
        addMessage(thread, "tutor", text, provider);
        controller.enqueue(line({ done: true }));
      } catch (e) {
        controller.enqueue(line({ error: (e as Error).message }));
      }
      controller.close();
    },
  });
  return new Response(stream, { headers: { "Content-Type": "application/x-ndjson; charset=utf-8", "Cache-Control": "no-store" } });
}
