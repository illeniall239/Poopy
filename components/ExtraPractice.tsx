"use client";
import { useState, useTransition } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { generateExtraExercise } from "@/app/actions";
import { dotClass } from "@/lib/status-ui";
import type { ExerciseStatus } from "@/lib/progress";

type Extra = { id: string; title: string; difficulty: string; status: ExerciseStatus };

export function ExtraPractice({ topicId, extras }: { topicId: string; extras: Extra[] }) {
  const router = useRouter();
  const [pending, start] = useTransition();
  const [error, setError] = useState<string | null>(null);

  function generate() {
    setError(null);
    start(async () => {
      try {
        const { id } = await generateExtraExercise(topicId);
        router.push(`/exercises/${id}`);
      } catch (e) {
        setError((e as Error).message);
      }
    });
  }

  return (
    <div className="panel grid gap-3 p-5">
      <p className="eyebrow">Dig deeper</p>
      {extras.length > 0 && (
        <ul className="grid gap-1.5">
          {extras.map((e) => (
            <li key={e.id} className="flex items-center justify-between gap-2 text-sm">
              <Link href={`/exercises/${e.id}`} className="hover:text-accent">{e.title} <span className="text-muted">· {e.difficulty}</span></Link>
              <span className={`size-2 rounded-full ${dotClass[e.status]}`} aria-hidden />
            </li>
          ))}
        </ul>
      )}
      <p className="text-xs text-muted">The Tutor writes a new exercise on this topic in your current language and checks its tests before showing it. Extras don&apos;t count towards the topic being learned.</p>
      <button onClick={generate} disabled={pending} className="btn justify-self-start">{pending ? "Writing and checking… (about a minute)" : "Generate another exercise"}</button>
      {error && <p className="rounded bg-bad-soft px-3 py-2 text-sm" role="alert">{error}</p>}
    </div>
  );
}
