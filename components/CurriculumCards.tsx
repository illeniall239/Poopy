import Link from "next/link";
import type { Phase, Topic } from "@/lib/curriculum.ts";
import type { ExerciseState, TopicState } from "@/lib/progress.ts";
import { exerciseStatus, isTopicLearned } from "@/lib/progress.ts";
import { dotClass } from "@/lib/status-ui.ts";

type Props = {
  phases: Phase[];
  topics: Topic[];
  topicStates: Map<string, TopicState>;
  exerciseStates: Map<string, ExerciseState>;
  currentTopicId: string | null;
  today: string;
};

// The whole Curriculum Map as cards: one per phase; the current phase is open, others expand on click.
export function CurriculumCards({ phases, topics, topicStates, exerciseStates, currentTopicId, today }: Props) {
  const learned = (t: Topic) => isTopicLearned(t, topicStates.get(t.id), exerciseStates, today);
  const currentPhase = topics.find((t) => t.id === currentTopicId)?.phase ?? phases[0]?.number;

  return (
    <section className="grid gap-4" aria-labelledby="curriculum">
      <h2 id="curriculum" className="font-display text-2xl font-semibold">Curriculum</h2>
      {phases.map((phase) => {
        const inPhase = topics.filter((t) => t.phase === phase.number);
        const done = inPhase.filter(learned).length;
        const isCurrent = phase.number === currentPhase;
        return (
          <details key={phase.number} open={isCurrent} className={`panel group ${isCurrent ? "border-accent" : ""}`}>
            <summary className="flex cursor-pointer list-none flex-wrap items-center gap-x-6 gap-y-2 p-5 [&::-webkit-details-marker]:hidden">
              <span className="font-mono text-sm text-muted">Phase {phase.number}</span>
              <span className="font-display text-lg font-semibold">{phase.title}</span>
              {isCurrent && <span className="chip bg-accent text-panel">You are here</span>}
              <span className="ml-auto flex items-center gap-3">
                <span className="font-mono text-xs text-muted">{done}/{inPhase.length} learned</span>
                <span className="h-1.5 w-28 overflow-hidden rounded-full bg-line" aria-hidden>
                  <span className="block h-full rounded-full bg-accent" style={{ width: `${(done / inPhase.length) * 100}%` }} />
                </span>
                <span className="text-muted transition-transform group-open:rotate-90" aria-hidden>›</span>
              </span>
            </summary>
            <ol className="grid gap-3 border-t border-line p-5 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
              {inPhase.map((t) => {
                const isLearned = learned(t);
                const isNow = t.id === currentTopicId;
                return (
                  <li key={t.id}>
                    <Link
                      href={`/topics/${t.id}`}
                      aria-current={isNow ? "step" : undefined}
                      className={`grid h-full content-start gap-2 rounded-lg border p-4 transition-colors hover:border-accent ${isNow ? "border-accent bg-accent-soft" : "border-line"}`}
                    >
                      <span className="flex items-center justify-between gap-2">
                        <span className="font-mono text-xs text-muted">{t.id}</span>
                        {isLearned ? (
                          <span className="chip bg-accent text-panel">Learned</span>
                        ) : isNow ? (
                          <span className="chip bg-accent text-panel">Now</span>
                        ) : topicStates.get(t.id)?.teach_done_at ? (
                          <span className="chip bg-warn-soft text-warn">In progress</span>
                        ) : null}
                      </span>
                      <span className={`font-semibold leading-snug ${isLearned ? "text-muted" : ""}`}>{t.title}</span>
                      {t.exerciseIds.length > 0 ? (
                        <span className="flex gap-1" aria-label={`${t.exerciseIds.length} exercises`}>
                          {t.exerciseIds.map((id) => <span key={id} className={`size-2 rounded-full ${dotClass[exerciseStatus(exerciseStates.get(id), today)]}`} />)}
                        </span>
                      ) : (
                        <span className="text-xs text-muted">Project practice</span>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ol>
          </details>
        );
      })}
    </section>
  );
}
