"use client";
import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { reviewProject } from "@/app/actions";
import type { ReviewResult } from "@/lib/projects";

type Past = { id: number; folder: string; when: string; result: ReviewResult };

export function ProjectReviewPanel({ topicId, taught, history }: { topicId: string; taught: boolean; history: Past[] }) {
  const router = useRouter();
  const [folder, setFolder] = useState(history[0]?.folder ?? "");
  const [latest, setLatest] = useState<(ReviewResult & { topicLearned?: boolean }) | null>(history[0]?.result ?? null);
  const [error, setError] = useState<string | null>(null);
  const [pending, start] = useTransition();

  function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    start(async () => {
      try {
        setLatest(await reviewProject(topicId, folder));
        router.refresh();
      } catch (err) {
        setError((err as Error).message);
      }
    });
  }

  return (
    <div className="panel grid gap-3 p-5">
      <p className="eyebrow">Project review</p>
      {!taught && <p className="text-sm text-muted">Finish the lesson first, then do the practice task and bring it here.</p>}
      <form onSubmit={submit} className="grid gap-2">
        <label htmlFor={`folder-${topicId}`} className="text-sm font-semibold">Your project folder</label>
        <input
          id={`folder-${topicId}`}
          value={folder}
          onChange={(e) => setFolder(e.target.value)}
          placeholder="C:\Users\you\projects\my-api"
          className="field font-mono text-sm"
          required
        />
        <p className="text-xs text-muted">
          Source and config files are read and sent to the Tutor. Skipped: node_modules, builds, .git, lockfiles, binaries and .env files; values that look like passwords or keys are masked.
        </p>
        <button type="submit" disabled={pending || !taught} className="btn btn-primary justify-self-start">
          {pending ? "Reviewing… (up to a minute or two)" : "Review my project"}
        </button>
      </form>
      {error && <p className="rounded bg-bad-soft px-3 py-2 text-sm" role="alert">{error}</p>}
      {latest && (
        <div className={`grid gap-2 rounded-md p-3 text-[15px] ${latest.passed ? "bg-accent-soft" : "bg-warn-soft"}`} role="status">
          <p><strong>{latest.passed ? "Passed." : "Not yet."}</strong> {latest.summary}</p>
          {latest.topicLearned && <p className="font-semibold">Topic {topicId} is now learned. Its first spaced review is tomorrow.</p>}
          {latest.issues.length > 0 && (
            <div className="grid gap-1">
              <p className="text-sm font-semibold">Issues</p>
              <ul className="grid gap-1 text-sm">{latest.issues.map((i, n) => <li key={n}><code className="font-mono text-xs">{i.file}</code> — {i.note}</li>)}</ul>
            </div>
          )}
          {latest.questions.length > 0 && (
            <div className="grid gap-1">
              <p className="text-sm font-semibold">Think about</p>
              <ul className="grid list-disc gap-1 pl-5 text-sm">{latest.questions.map((q, n) => <li key={n}>{q}</li>)}</ul>
            </div>
          )}
          {latest.strengths.length > 0 && (
            <div className="grid gap-1">
              <p className="text-sm font-semibold">Good</p>
              <ul className="grid list-disc gap-1 pl-5 text-sm">{latest.strengths.map((s, n) => <li key={n}>{s}</li>)}</ul>
            </div>
          )}
        </div>
      )}
      {history.length > 1 && <p className="text-xs text-muted">{history.length} reviews so far · last: {history[0].when.slice(0, 16)}</p>}
    </div>
  );
}
