import Link from "next/link";
import { connection } from "next/server";
import { loadCurriculum } from "@/lib/curriculum.ts";
import { allDays, allExerciseStates, allReviews, allTopicStates, getDay, getMessages } from "@/lib/db.ts";
import { currentStreak, exerciseStatus, isTopicLearned, localToday, planToday, type PlanItem } from "@/lib/progress.ts";
import { dotClass } from "@/components/Sidebar";

const statusLabel: Record<string, string> = {
  new: "Not started",
  in_progress: "In progress",
  needs_explain: "Explain your solution",
};

export default async function Today() {
  await connection();
  const today = localToday();
  const { topics, exercises } = loadCurriculum();
  const topicStates = allTopicStates();
  const exerciseStates = allExerciseStates();
  const reviewsAll = allReviews();
  const plan = planToday(topics, topicStates, exerciseStates, reviewsAll, today);
  const topicOf = (id: string) => topics.find((t) => t.id === id)!;

  const learned = topics.filter((t) => isTopicLearned(t, topicStates.get(t.id), exerciseStates, today)).length;
  const exercisesDone = [...exercises.keys()].filter((id) => exerciseStatus(exerciseStates.get(id), today) === "done").length;

  const keptDays = new Set(allDays().filter((d) => d.kept).map((d) => d.date));
  const streak = currentStreak(keptDays, today);
  const keptToday = keptDays.has(today);
  const passedToday = !!getDay(today)?.exercise_passed;
  const reviews = plan.filter((p): p is Extract<PlanItem, { kind: "review" }> => p.kind === "review");
  const retries = plan.filter((p): p is Extract<PlanItem, { kind: "retry" }> => p.kind === "retry");
  const teach = plan.find((p): p is Extract<PlanItem, { kind: "teach" }> => p.kind === "teach");
  const practiceItem = plan.find((p): p is Extract<PlanItem, { kind: "practice" }> => p.kind === "practice");
  const exerciseItems = plan.filter((p): p is Extract<PlanItem, { kind: "exercise" }> => p.kind === "exercise");
  const currentTopic = teach ? topicOf(teach.topicId) : practiceItem ? topicOf(practiceItem.topicId) : exerciseItems[0] ? topicOf(exercises.get(exerciseItems[0].exerciseId)!.topicId) : null;

  return (
    <main className="grid gap-8 px-6 py-8 xl:px-10">
      <header className="flex flex-wrap items-end justify-between gap-6">
        <div className="grid gap-1">
          <p className="eyebrow">{new Date(`${today}T12:00:00`).toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" })}</p>
          <h1 className="font-display text-4xl font-bold">Today&apos;s Session</h1>
        </div>
        <dl className="grid grid-cols-2 gap-3 sm:grid-cols-5">
          <Stat label="Streak" value={`${streak}d`} />
          <Stat label="Reviews due" value={reviews.length} />
          <Stat label="Come-backs" value={retries.length} />
          <Stat label="Topics learned" value={`${learned}/${topics.length}`} />
          <Stat label="Exercises done" value={`${exercisesDone}/${exercises.size}`} />
        </dl>
      </header>

      {!keptToday && (
        <p className="rounded-md bg-warn-soft px-4 py-3 text-[15px]" role="status">
          <strong>{streak > 0 ? `Keep your ${streak}-day streak:` : "Start a streak:"}</strong>{" "}
          {[!passedToday && "pass one exercise", reviews.length > 0 && `clear ${reviews.length} due review${reviews.length === 1 ? "" : "s"}`].filter(Boolean).join(" and ")} today.
        </p>
      )}

      <div className="grid gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
        {/* Up next: the main work of the Session */}
        <section className="panel grid content-start gap-5 p-6" aria-labelledby="next">
          <p id="next" className="eyebrow">Up next</p>
          {!currentTopic ? (
            <p className="text-muted">Everything available today is done. Take the recap.</p>
          ) : (
            <>
              <div className="grid gap-2">
                <h2 className="font-display text-3xl font-bold text-balance">
                  <span className="mr-3 font-mono text-lg text-muted">{currentTopic.id}</span>
                  {currentTopic.title}
                </h2>
                <p className="max-w-[75ch] text-muted">Goal: {currentTopic.learnedWhen}</p>
              </div>

              {teach ? (
                <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
                  <div className="grid gap-2">
                    <p className="text-sm font-semibold">What this lesson covers</p>
                    <ul className="grid gap-1.5 text-[15px] sm:grid-cols-2">
                      {currentTopic.teach.split(/;\s*/).map((c) => (
                        <li key={c} className="flex gap-2"><span className="text-accent" aria-hidden>›</span><span>{c.replace(/\.$/, "")}</span></li>
                      ))}
                    </ul>
                  </div>
                  <Link href={`/topics/${currentTopic.id}`} className="btn btn-primary px-5 py-3 text-base">{getMessages(`teach:${currentTopic.id}`).some((m) => m.role === "learner") ? "Continue the lesson" : "Start the lesson"}</Link>
                </div>
              ) : practiceItem ? (
                <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
                  <div className="grid gap-2">
                    <p className="text-sm font-semibold">Practice in your own project</p>
                    <p className="max-w-[75ch] text-[15px]">{currentTopic.practice}</p>
                  </div>
                  <Link href={`/topics/${currentTopic.id}`} className="btn btn-primary px-5 py-3 text-base">Get it reviewed</Link>
                </div>
              ) : (
                <div className="grid gap-3">
                  <p className="text-sm font-semibold">Exercises</p>
                  <div className="grid gap-3 md:grid-cols-3">
                    {currentTopic.exerciseIds.map((id, i) => {
                      const status = exerciseStatus(exerciseStates.get(id), today);
                      const open = exerciseItems.some((p) => p.exerciseId === id);
                      const ex = exercises.get(id)!;
                      return (
                        <Link key={id} href={`/exercises/${id}`} className={`panel grid gap-2 p-4 transition-colors hover:border-accent ${open ? "" : "opacity-60"}`}>
                          <span className="flex items-center justify-between font-mono text-xs text-muted">
                            Exercise {i + 1} · {ex.difficulty}
                            <span className={`size-2 rounded-full ${dotClass[status]}`} aria-hidden />
                          </span>
                          <span className="font-display text-lg font-semibold">{ex.title}</span>
                          <span className="text-sm text-muted">{statusLabel[status] ?? (status === "done" ? "Done" : "Comes back later")}</span>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </section>

        {/* Steps 1 and 3 */}
        <div className="grid content-start gap-6">
          <section className="panel grid gap-3 p-5" aria-labelledby="reviews">
            <p id="reviews" className="eyebrow">Spaced Reviews</p>
            {reviews.length === 0 ? (
              <p className="text-sm text-muted">
                Nothing due today.{reviewsAll.length ? ` Next one: ${reviewsAll[0].due_date}.` : " Reviews start once you've learned a topic."}
              </p>
            ) : (
              reviews.map((r) => (
                <Row key={r.topicId} href={`/review/${r.topicId}`} title={`${r.topicId} · ${topicOf(r.topicId).title}`} chip="Due" />
              ))
            )}
          </section>

          {retries.length > 0 && (
            <section className="panel grid gap-3 p-5" aria-labelledby="retries">
              <p id="retries" className="eyebrow">Come-back Exercises</p>
              <p className="text-sm text-muted">You solved these with help. Solve them again from scratch, no hints.</p>
              {retries.map((r) => (
                <Row key={r.exerciseId} href={`/exercises/${r.exerciseId}`} title={exercises.get(r.exerciseId)!.title} chip="Retry due" />
              ))}
            </section>
          )}

          <section className="panel grid gap-3 p-5" aria-labelledby="recap">
            <p id="recap" className="eyebrow">Recap</p>
            <p className="text-sm text-muted">Two minutes at the end: say what you learned and what was hardest.</p>
            <Link href="/recap" className="btn justify-self-start">Open the recap</Link>
          </section>
        </div>
      </div>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="panel min-w-32 px-4 py-3">
      <dt className="text-xs text-muted">{label}</dt>
      <dd className="font-mono text-2xl font-semibold tabular-nums">{value}</dd>
    </div>
  );
}

function Row({ href, title, chip }: { href: string; title: string; chip: string }) {
  return (
    <Link href={href} className="flex items-center justify-between gap-4 rounded-md border border-line px-3 py-2.5 transition-colors hover:border-accent">
      <span className="font-semibold">{title}</span>
      <span className="chip shrink-0 bg-accent-soft text-accent">{chip}</span>
    </Link>
  );
}
