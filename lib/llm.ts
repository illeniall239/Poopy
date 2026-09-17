// Model providers: Claude via the Learner's installed Claude Code (Pro login), and local Ollama (ADR 0002).
// Findings behind the flags used here: spikes/FINDINGS.md.
import { spawn } from "node:child_process";
import { getSetting } from "./db.ts";
import type { Language } from "./languages.ts";

export type ChatMessage = { role: "user" | "assistant"; content: string };
export type Provider = "claude" | "ollama";
export type ProviderMode = "auto" | Provider;

export const settingsDefaults = {
  providerMode: "auto" as ProviderMode,
  claudeModel: "sonnet",
  ollamaModel: "qwen3:14b",
  ollamaUrl: "http://127.0.0.1:11434",
  language: "typescript" as Language, // what the Learner writes Exercises in
};

const setting = <K extends keyof typeof settingsDefaults>(k: K) => getSetting(k, settingsDefaults[k]) as (typeof settingsDefaults)[K];

function providerOrder(): Provider[] {
  const mode = setting("providerMode");
  return mode === "auto" ? ["claude", "ollama"] : [mode];
}

// ---------- Claude Code ----------

function claudeBinary() {
  // Windows: `claude` is a .cmd shim Node can't spawn without a shell, so spawn the real exe.
  return process.platform === "win32"
    ? `${process.env.APPDATA}\\npm\\node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe`
    : "claude";
}

// Claude Code -p takes one prompt, so the conversation is rendered into it. History lives in our DB, not in Claude Code sessions.
function renderTranscript(messages: ChatMessage[]) {
  if (messages.length === 1) return messages[0].content;
  const [first, ...rest] = messages;
  return `${first.content}\n\n--- Conversation so far ---\n\n${rest
    .map((m) => `${m.role === "user" ? "Learner" : "Tutor"}: ${m.content}`)
    .join("\n\n")}\n\n--- End of conversation ---\nReply as the Tutor to the Learner's last message.`;
}

type ClaudeEvent = { type: string; event?: { delta?: { type: string; text?: string } }; is_error?: boolean; result?: string; structured_output?: unknown };

async function* claudeRun(system: string, messages: ChatMessage[], extraArgs: string[] = []): AsyncGenerator<ClaudeEvent> {
  const env = { ...process.env };
  delete env.CLAUDECODE;
  const child = spawn(
    claudeBinary(),
    [
      "-p", "--output-format", "stream-json", "--verbose", "--include-partial-messages",
      "--system-prompt", system,
      "--tools", "", "--strict-mcp-config", "--setting-sources", "", "--no-session-persistence",
      "--model", setting("claudeModel"),
      ...extraArgs,
    ],
    { env },
  );
  // Prompt goes through stdin: Windows caps command lines at ~32k characters.
  child.stdin.end(renderTranscript(messages));
  let stderr = "";
  child.stderr.on("data", (d) => (stderr += d));
  const exited = new Promise<number | null>((res) => child.on("close", res));
  const spawnError = new Promise<never>((_, rej) => child.on("error", rej));
  spawnError.catch(() => {}); // observed via the race below; avoid an unhandled rejection after we finish

  let buf = "";
  let sawResult = false;
  const iter = child.stdout[Symbol.asyncIterator]();
  try {
    while (true) {
      const next = await Promise.race([iter.next(), spawnError]);
      if (next.done) break;
      buf += next.value;
      let nl;
      while ((nl = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue;
        const ev = JSON.parse(line) as ClaudeEvent;
        if (ev.type === "result") {
          sawResult = true;
          if (ev.is_error) throw new Error(`Claude: ${ev.result ?? "error"}`);
        }
        yield ev;
      }
    }
    const code = await exited;
    if (!sawResult) throw new Error(`Claude Code exited (${code}): ${stderr.slice(0, 300) || "no output"}`);
  } finally {
    if (child.exitCode === null) child.kill(); // the consumer stopped early or something failed
  }
}

async function* claudeStream(system: string, messages: ChatMessage[]) {
  for await (const ev of claudeRun(system, messages)) {
    if (ev.type === "stream_event" && ev.event?.delta?.type === "text_delta" && ev.event.delta.text) yield ev.event.delta.text;
  }
}

async function claudeJson(system: string, messages: ChatMessage[], schema: object): Promise<unknown> {
  let out: unknown;
  for await (const ev of claudeRun(system, messages, ["--json-schema", JSON.stringify(schema)])) {
    if (ev.type === "result") out = ev.structured_output;
  }
  if (out === undefined) throw new Error("Claude returned no structured output");
  return out;
}

// ---------- Ollama ----------

async function ollamaFetch(system: string, messages: ChatMessage[], extra: object) {
  const res = await fetch(`${setting("ollamaUrl")}/api/chat`, {
    method: "POST",
    body: JSON.stringify({
      model: setting("ollamaModel"),
      think: false,
      keep_alive: "30m",
      messages: [{ role: "system", content: system }, ...messages],
      ...extra,
    }),
  }).catch((e) => {
    throw new Error(`Ollama isn't reachable at ${setting("ollamaUrl")} — is it running? (${e.message})`);
  });
  if (!res.ok) throw new Error(`Ollama: ${res.status} ${await res.text()}`);
  return res;
}

async function* ollamaStream(system: string, messages: ChatMessage[]) {
  const res = await ollamaFetch(system, messages, { stream: true });
  const reader = res.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buf = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += value;
    let nl;
    while ((nl = buf.indexOf("\n")) >= 0) {
      const ev = JSON.parse(buf.slice(0, nl));
      buf = buf.slice(nl + 1);
      if (ev.error) throw new Error(`Ollama: ${ev.error}`);
      if (ev.message?.content) yield ev.message.content as string;
    }
  }
}

async function ollamaJson(system: string, messages: ChatMessage[], schema: object): Promise<unknown> {
  const res = await ollamaFetch(system, messages, { stream: false, format: schema });
  const body = await res.json();
  return JSON.parse(body.message.content);
}

// ---------- Public API with fallback ----------

export type StreamChunk = { provider: Provider } | { text: string } | { notice: string };

// Streams a reply. In auto mode, a Claude failure before any text arrives (e.g. the Pro usage limit) falls back to Ollama.
export async function* streamReply(system: string, messages: ChatMessage[]): AsyncGenerator<StreamChunk> {
  const errors: string[] = [];
  for (const provider of providerOrder()) {
    let started = false;
    try {
      const gen = provider === "claude" ? claudeStream(system, messages) : ollamaStream(system, messages);
      for await (const text of gen) {
        if (!started) {
          started = true;
          if (errors.length) yield { notice: `Claude unavailable, switched to local model. (${errors[0]})` };
          yield { provider };
        }
        yield { text };
      }
      if (started) return;
      errors.push(`${provider} returned an empty reply`);
    } catch (e) {
      if (started) throw e;
      errors.push((e as Error).message);
    }
  }
  throw new Error(errors.join(" | "));
}

export async function jsonReply<T>(system: string, messages: ChatMessage[], schema: object): Promise<{ value: T; provider: Provider }> {
  const errors: string[] = [];
  for (const provider of providerOrder()) {
    try {
      const value = provider === "claude" ? await claudeJson(system, messages, schema) : await ollamaJson(system, messages, schema);
      return { value: value as T, provider };
    } catch (e) {
      errors.push((e as Error).message);
    }
  }
  throw new Error(errors.join(" | "));
}
