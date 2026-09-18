import { connection } from "next/server";
import { loadCurriculum } from "@/lib/curriculum.ts";
import { allMistakes } from "@/lib/db.ts";
import { addMistake } from "@/app/actions.ts";
import { MistakeRow } from "@/components/MistakeRow";

export default async function MistakesPage() {
  await connection();
  const { topics } = loadCurriculum();
  const mistakes = allMistakes();
  const title = (id: string | null) => (id ? `${id} · ${topics.find((t) => t.id === id)?.title ?? ""}` : "General");
  const groups = [...new Set(mistakes.map((m) => m.topic_id))].sort((a, b) => (a ?? "~").localeCompare(b ?? "~", undefined, { numeric: true }));

  return (
    <main className="grid content-start gap-6 px-6 py-8 xl:px-10">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div className="grid gap-1">
          <p className="eyebrow">Mistake log</p>
          <h1 className="font-display text-4xl font-bold">Your recurring mistakes</h1>
          <p className="max-w-[70ch] text-muted">
            Collected from explain-backs, spaced reviews and interviews. The Tutor aims review questions and extra exercises at these.
            Edit any that are wrong, delete ones you&apos;ve fixed, or add your own.
          </p>
        </div>
      </header>

      <form action={addMistake} className="panel flex flex-wrap items-end gap-3 p-4">
        <div className="grid min-w-64 flex-1 gap-1">
          <label htmlFor="mistake-text" className="text-sm font-semibold">Add a mistake you keep making</label>
          <input id="mistake-text" name="text" required className="field" placeholder="e.g. I start loops at 1 instead of 0" />
        </div>
        <div className="grid gap-1">
          <label htmlFor="mistake-topic" className="text-sm font-semibold">Topic</label>
          <select id="mistake-topic" name="topic" className="field">
            <option value="">General</option>
            {topics.map((t) => <option key={t.id} value={t.id}>{t.id} · {t.title}</option>)}
          </select>
        </div>
        <button type="submit" className="btn btn-primary">Add</button>
      </form>

      {mistakes.length === 0 ? (
        <p className="text-muted">Nothing logged yet. Mistakes appear here after explain-backs, spaced reviews and interviews.</p>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {groups.map((g) => (
            <section key={g ?? "general"} className="panel grid content-start gap-2 p-5">
              <h2 className="font-display text-lg font-semibold">{title(g)}</h2>
              <ul className="grid gap-2">
                {mistakes.filter((m) => m.topic_id === g).map((m) => (
                  <MistakeRow key={m.id} id={m.id} text={m.text} count={m.count} source={m.source} />
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}
    </main>
  );
}
