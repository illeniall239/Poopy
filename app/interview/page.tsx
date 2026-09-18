import Link from "next/link";
import { connection } from "next/server";
import { allInterviews } from "@/lib/db.ts";
import { INTERVIEW_KINDS, isInterviewKind, type Feedback, type InterviewKind } from "@/lib/interview.ts";
import { startInterview } from "@/app/actions.ts";

const ratingClass: Record<string, string> = {
  "strong hire": "bg-accent text-panel",
  hire: "bg-accent-soft text-accent",
  "lean no hire": "bg-warn-soft text-warn",
  "no hire": "bg-bad-soft text-bad",
};

export default async function InterviewPage() {
  await connection();
  const past = allInterviews();

  return (
    <main className="grid content-start gap-8 px-6 py-8 xl:px-10">
      <header className="grid gap-1">
        <p className="eyebrow">Interview practice</p>
        <h1 className="font-display text-4xl font-bold">Mock interviews</h1>
        <p className="max-w-[70ch] text-muted">
          Separate from your daily Session and open any time. Problems can come from any topic, learned or not. Feedback is written
          like a real panel&apos;s, and the mistakes it finds go into your mistake log.
        </p>
      </header>

      <section className="grid gap-4 md:grid-cols-2 2xl:grid-cols-4" aria-label="Start an interview">
        {(Object.entries(INTERVIEW_KINDS) as [InterviewKind, (typeof INTERVIEW_KINDS)[InterviewKind]][]).map(([kind, k]) => (
          <form key={kind} action={startInterview.bind(null, kind)} className="panel grid content-between gap-4 p-5">
            <div className="grid gap-2">
              <h2 className="font-display text-xl font-semibold">{k.label}</h2>
              <p className="font-mono text-xs text-muted">{k.minutes} minutes</p>
              <p className="text-[15px] text-muted">{k.blurb}</p>
            </div>
            <button type="submit" className="btn btn-primary justify-self-start">Start</button>
          </form>
        ))}
      </section>

      <section className="grid gap-3" aria-labelledby="past">
        <h2 id="past" className="font-display text-2xl font-semibold">Past interviews</h2>
        {past.length === 0 ? (
          <p className="text-muted">None yet.</p>
        ) : (
          <ul className="grid gap-2">
            {past.map((iv) => {
              const fb = iv.feedback ? (JSON.parse(iv.feedback) as Feedback) : null;
              return (
                <li key={iv.id}>
                  <Link href={`/interview/${iv.id}`} className="panel flex flex-wrap items-center gap-4 px-4 py-3 transition-colors hover:border-accent">
                    <span className="font-semibold">{isInterviewKind(iv.kind) ? INTERVIEW_KINDS[iv.kind].label : iv.kind}</span>
                    <span className="font-mono text-xs text-muted">{iv.started_at.slice(0, 16)}</span>
                    <span className="ml-auto">
                      {fb ? <span className={`chip ${ratingClass[fb.rating] ?? "bg-line"}`}>{fb.rating}</span> : <span className="chip bg-line text-muted">in progress</span>}
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </main>
  );
}
