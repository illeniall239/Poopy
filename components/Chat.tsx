"use client";
import { useEffect, useRef, useState } from "react";
import { Markdown } from "./Markdown";
import type { ChatKind, RunInfo } from "@/lib/tutor";

export type ChatMessageView = { role: "learner" | "tutor"; content: string; provider?: string | null };

type Props = {
  kind: ChatKind;
  id: string;
  initial: ChatMessageView[];
  autoStart?: boolean; // ask the Tutor to open the conversation when it's empty
  placeholder?: string;
  getContext?: () => { code?: string; lastRun?: RunInfo };
  onTutorReply?: (text: string) => void;
  emptyText?: string;
};

export function Chat({ kind, id, initial, autoStart = false, placeholder = "Reply to the Tutor…", getContext, onTutorReply, emptyText }: Props) {
  const [messages, setMessages] = useState<ChatMessageView[]>(initial);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const started = useRef(false);

  useEffect(() => {
    bottom.current?.scrollIntoView({ block: "end" });
  }, [messages]);

  async function send(message?: string) {
    setBusy(true);
    setError(null);
    setNotice(null);
    if (message) setMessages((m) => [...m, { role: "learner", content: message }]);
    setMessages((m) => [...m, { role: "tutor", content: "" }]);
    let text = "";
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kind, id, message, ...getContext?.() }),
      });
      if (!res.ok || !res.body) throw new Error(await res.text());
      const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += value;
        let nl;
        while ((nl = buf.indexOf("\n")) >= 0) {
          const ev = JSON.parse(buf.slice(0, nl));
          buf = buf.slice(nl + 1);
          if (ev.error) throw new Error(ev.error);
          if (ev.notice) setNotice(ev.notice);
          if (ev.text || ev.provider) {
            if (ev.text) text += ev.text;
            setMessages((m) => {
              const last = m[m.length - 1];
              return [...m.slice(0, -1), { ...last, content: text, provider: ev.provider ?? last.provider }];
            });
          }
        }
      }
      onTutorReply?.(text);
    } catch (e) {
      setError((e as Error).message);
      setMessages((m) => (m[m.length - 1]?.role === "tutor" && !m[m.length - 1].content ? m.slice(0, -1) : m));
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (autoStart && !started.current && initial.length === 0) {
      started.current = true;
      void send();
    }
  }, [autoStart, kind, id]);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const message = draft.trim();
    if (!message || busy) return;
    setDraft("");
    void send(message);
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="min-h-0 flex-1 space-y-4 overflow-y-auto pr-1" aria-live="polite">
        {messages.length === 0 && !busy && emptyText && <p className="text-sm text-muted">{emptyText}</p>}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "learner" ? "ml-8 rounded-lg bg-accent-soft px-3 py-2" : ""}>
            <div className="mb-1 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wider text-muted">
              {m.role === "learner" ? "You" : "Tutor"}
              {m.provider && <span className="rounded bg-line px-1.5 py-px font-mono normal-case tracking-normal">{m.provider}</span>}
            </div>
            {m.content ? <Markdown text={m.content} /> : <p className="animate-pulse text-sm text-muted">Thinking…</p>}
          </div>
        ))}
        <div ref={bottom} />
      </div>
      {notice && <p className="mt-2 rounded bg-warn-soft px-3 py-2 text-sm">{notice}</p>}
      {error && <p className="mt-2 rounded bg-bad-soft px-3 py-2 text-sm" role="alert">{error}</p>}
      <form onSubmit={submit} className="mt-3 flex gap-2">
        <label htmlFor={`chat-${kind}-${id}`} className="sr-only">Message</label>
        <textarea
          id={`chat-${kind}-${id}`}
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) submit(e); }}
          placeholder={placeholder}
          rows={2}
          className="field flex-1 resize-none"
        />
        <button type="submit" disabled={busy || !draft.trim()} className="btn btn-primary self-end">Send</button>
      </form>
    </div>
  );
}
