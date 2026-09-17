import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { connection } from "next/server";
import { getExercise, getTopic } from "@/lib/curriculum.ts";
import { allExerciseStates, allTopicStates, getMessages } from "@/lib/db.ts";
import { exerciseStatus, localToday } from "@/lib/progress.ts";
import { threadFor } from "@/lib/tutor.ts";
import { markTeachDone } from "@/app/actions.ts";
import { Chat } from "@/components/Chat";
import { dotClass } from "@/components/Sidebar";

export default async function TopicPage(props: PageProps<"/topics/[id]">) {
  await connection();
  const { id } = await props.params;
  const topic = getTopic(id);
  if (!topic) notFound();
  const taught = !!allTopicStates().get(id)?.teach_done_at;
  const states = allExerciseStates();
  const messages = getMessages(threadFor("teach", id)).map((m) => ({ role: m.role, content: m.content, provider: m.provider }));

  async function startExercises() {
    "use server";
    await markTeachDone(id);
    redirect(`/exercises/${topic!.exerciseIds[0]}`);
  }

  return (
    <main className="grid gap-6 p-6 lg:h-screen lg:grid-cols-[minmax(0,1fr)_340px] xl:px-10">
      <section className="flex min-h-[70vh] flex-col gap-4 lg:min-h-0">
        <header className="grid gap-1">
          <p className="eyebrow">Topic {topic.id} · lesson</p>
          <h1 className="font-display text-3xl font-bold text-balance">{topic.title}</h1>
        </header>
        <div className="panel min-h-0 flex-1 p-5">
          <Chat kind="teach" id={id} initial={messages} autoStart placeholder="Answer the Tutor's question… (Enter to send, Shift+Enter for a new line)" />
        </div>
      </section>

      <aside className="grid content-start gap-4 lg:overflow-y-auto">
        <div className="panel grid gap-2 p-5">
          <p className="eyebrow">Goal</p>
          <p className="text-[15px]">{topic.learnedWhen}</p>
        </div>
        <div className="panel grid gap-2 p-5">
          <p className="eyebrow">This lesson covers</p>
          <ul className="grid gap-1.5 text-[15px]">
            {topic.teach.split(/;\s*/).map((c) => (
              <li key={c} className="flex gap-2"><span className="text-accent" aria-hidden>›</span><span>{c.replace(/\.$/, "")}</span></li>
            ))}
          </ul>
        </div>
        <div className="panel grid gap-3 p-5">
          <p className="eyebrow">Then practise</p>
          <ul className="grid gap-1.5">
            {topic.exerciseIds.map((exId) => (
              <li key={exId} className="flex items-center justify-between gap-2 text-sm">
                <Link href={`/exercises/${exId}`} className="hover:text-accent">{getExercise(exId)?.title}</Link>
                <span className={`size-2 rounded-full ${dotClass[exerciseStatus(states.get(exId), localToday())]}`} aria-hidden />
              </li>
            ))}
          </ul>
          <form action={startExercises} className="grid gap-2 border-t border-line pt-3">
            <button type="submit" className="btn btn-primary">Start exercises</button>
            <p className="text-xs text-muted">
              {taught ? "Lesson finished. You can still ask questions here." : "Press this when the Tutor says you're ready."}
            </p>
          </form>
        </div>
      </aside>
    </main>
  );
}
