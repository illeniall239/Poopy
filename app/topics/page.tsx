import Link from "next/link";
import { connection } from "next/server";
import { loadCurriculum } from "@/lib/curriculum.ts";
import { allExerciseStates, allReviews, allTopicStates } from "@/lib/db.ts";
import { exerciseStatus, isTopicLearned, localToday, type ExerciseStatus } from "@/lib/progress.ts";

const chip: Record<ExerciseStatus, [string, string]> = {
  new: ["Not started", "bg-line text-muted"],
  in_progress: ["In progress", "bg-warn-soft text-warn"],
  needs_explain: ["Explain it", "bg-warn-soft text-warn"],
  waiting_retry: ["Comes back later", "bg-line text-muted"],
  retry_due: ["Retry due", "bg-bad-soft text-bad"],
  done: ["Done", "bg-accent-soft text-accent"],
};

export default async function Topics() {
  await connection();
  const today = localToday();
  const { topics, exercises } = loadCurriculum();
  const topicStates = allTopicStates();
  const states = allExerciseStates();
  const reviews = new Map(allReviews().map((r) => [r.topic_id, r]));

  return (
    <main className="grid gap-6 px-6 py-8 xl:px-10">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div className="grid gap-1">
          <p className="eyebrow">Curriculum Map · Phase 1</p>
          <h1 className="font-display text-4xl font-bold">All topics</h1>
        </div>
        <p className="text-sm text-muted">Phases 2–8 get their exercises when you reach them. Full map: <code className="font-mono">curriculum/MAP.md</code></p>
      </header>
      <ol className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        {topics.map((t) => {
          const learned = isTopicLearned(t, topicStates.get(t.id), states, today);
          const review = reviews.get(t.id);
          return (
            <li key={t.id} className="panel grid content-start gap-3 p-5">
              <div className="flex items-start justify-between gap-3">
                <Link href={`/topics/${t.id}`} className="font-display text-lg font-semibold leading-snug hover:text-accent">
                  <span className="mr-2 font-mono text-sm text-muted">{t.id}</span>
                  {t.title}
                </Link>
                {learned ? (
                  <span className="chip shrink-0 bg-accent text-panel">Learned</span>
                ) : topicStates.get(t.id)?.teach_done_at ? (
                  <span className="chip shrink-0 bg-warn-soft text-warn">Lesson done</span>
                ) : null}
              </div>
              <p className="text-sm text-muted">{t.learnedWhen}</p>
              {review && <p className="font-mono text-xs text-muted">Next review {review.due_date}</p>}
              <ul className="grid gap-1.5 border-t border-line pt-3">
                {t.exerciseIds.map((id) => {
                  const [label, cls] = chip[exerciseStatus(states.get(id), today)];
                  return (
                    <li key={id} className="flex items-center justify-between gap-3 text-sm">
                      <Link href={`/exercises/${id}`} className="hover:text-accent">{exercises.get(id)?.title}</Link>
                      <span className={`chip ${cls}`}>{label}</span>
                    </li>
                  );
                })}
              </ul>
            </li>
          );
        })}
      </ol>
    </main>
  );
}
