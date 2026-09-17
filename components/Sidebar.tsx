import { loadCurriculum } from "@/lib/curriculum.ts";
import { allExerciseStates, allTopicStates } from "@/lib/db.ts";
import { exerciseStatus, isTopicLearned, localToday, type ExerciseStatus } from "@/lib/progress.ts";
import { NavLink, TopicLink } from "./NavLink";
import { SidebarToggle } from "./SidebarToggle";

export const dotClass: Record<ExerciseStatus, string> = {
  new: "bg-line",
  in_progress: "bg-warn",
  needs_explain: "bg-warn",
  waiting_retry: "bg-muted",
  retry_due: "bg-bad",
  done: "bg-accent",
};

export function Sidebar({ collapsed = false }: { collapsed?: boolean }) {
  const today = localToday();
  const { topics, exercises } = loadCurriculum();
  const topicStates = allTopicStates();
  const states = allExerciseStates();
  const learned = topics.filter((t) => isTopicLearned(t, topicStates.get(t.id), states, today)).length;
  const done = [...exercises.keys()].filter((id) => exerciseStatus(states.get(id), today) === "done").length;
  const current = topics.find((t) => !isTopicLearned(t, topicStates.get(t.id), states, today));

  if (collapsed) {
    return (
      <aside className="hidden flex-col items-center gap-4 border-r border-line bg-panel py-4 lg:flex lg:h-screen">
        <SidebarToggle collapsed />
        <span className="font-display text-lg font-bold" title="Poopy">P</span>
        <div className="h-24 w-1.5 overflow-hidden rounded-full bg-line" role="progressbar" aria-valuenow={done} aria-valuemax={exercises.size} aria-label="Exercises done" title={`${done}/${exercises.size} exercises`}>
          <div className="w-full rounded-full bg-accent" style={{ height: `${(done / exercises.size) * 100}%` }} />
        </div>
        {current && <span className="font-mono text-xs font-bold text-accent" title={`Current topic: ${current.title}`}>{current.id}</span>}
      </aside>
    );
  }

  return (
    <aside className="flex flex-col gap-6 border-line bg-panel p-4 lg:h-screen lg:overflow-y-auto lg:overflow-x-hidden lg:border-r">
      <div className="flex items-start justify-between gap-2 pl-3 pt-2">
        <div className="grid gap-0.5">
          <span className="font-display text-xl font-bold">Poopy</span>
          <span className="text-xs text-muted">Phase 1 · Problem solving and TypeScript</span>
        </div>
        <SidebarToggle collapsed={false} />
      </div>

      <nav className="grid gap-0.5" aria-label="Main">
        <NavLink href="/">Today</NavLink>
        <NavLink href="/topics">All topics</NavLink>
        <NavLink href="/recap">Recap</NavLink>
        <NavLink href="/settings">Settings</NavLink>
      </nav>

      <div className="grid gap-2 px-3">
        <div className="flex justify-between font-mono text-xs text-muted">
          <span>{learned}/{topics.length} topics</span>
          <span>{done}/{exercises.size} exercises</span>
        </div>
        <div className="h-1.5 overflow-hidden rounded-full bg-line" role="progressbar" aria-valuenow={done} aria-valuemax={exercises.size} aria-label="Exercises done">
          <div className="h-full rounded-full bg-accent" style={{ width: `${(done / exercises.size) * 100}%` }} />
        </div>
      </div>

      <div className="hidden min-h-0 gap-0.5 lg:grid">
        <p className="eyebrow px-3 pb-1">Curriculum</p>
        {topics.map((t) => {
          const isLearned = isTopicLearned(t, topicStates.get(t.id), states, today);
          return (
            <TopicLink key={t.id} href={`/topics/${t.id}`} className="group flex items-start gap-3 rounded-md px-3 py-1.5">
              <span className={`w-7 shrink-0 font-mono text-xs ${t.id === current?.id ? "font-bold text-accent" : "text-muted"}`}>{t.id}</span>
              <span className={`min-w-0 flex-1 text-sm leading-snug ${isLearned ? "text-muted line-through decoration-line" : t.id === current?.id ? "font-semibold" : ""}`}>
                {t.title}
              </span>
              <span className="flex shrink-0 gap-1 pt-2" aria-hidden>
                {t.exerciseIds.map((id) => (
                  <span key={id} className={`size-1.5 rounded-full ${dotClass[exerciseStatus(states.get(id), today)]}`} />
                ))}
              </span>
            </TopicLink>
          );
        })}
      </div>
    </aside>
  );
}
