"use client";
import { useEffect, useRef, useState } from "react";
import { Markdown } from "./Markdown";

// Streams the Breakdown the first time it's opened; after that the saved one comes back instantly.
export function BreakdownView({ exerciseId, initial, active }: { exerciseId: string; initial: string | null; active: boolean }) {
  const [text, setText] = useState(initial ?? "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const started = useRef(false);

  useEffect(() => {
    if (!active || initial || started.current) return;
    started.current = true;
    void (async () => {
      setLoading(true);
      let acc = "";
      try {
        const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ kind: "breakdown", id: exerciseId }) });
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
            if (ev.text) setText((acc += ev.text));
          }
        }
      } catch (e) {
        setError((e as Error).message);
        started.current = false;
      } finally {
        setLoading(false);
      }
    })();
  }, [active, exerciseId, initial]);

  return (
    <article className="panel min-h-0 overflow-y-auto p-6 lg:p-8">
      <p className="eyebrow mb-4">Breakdown</p>
      {text ? <Markdown text={text} className="max-w-[80ch]" /> : loading ? <p className="animate-pulse text-muted">Writing the breakdown of this problem and its solution…</p> : null}
      {error && <p className="mt-4 rounded bg-bad-soft px-3 py-2 text-sm" role="alert">{error}</p>}
    </article>
  );
}
