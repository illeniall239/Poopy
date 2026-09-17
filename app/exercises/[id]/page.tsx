import { notFound } from "next/navigation";
import { connection } from "next/server";
import { getExercise, getTopic } from "@/lib/curriculum.ts";
import { LANGUAGES, currentLanguage, type Language } from "@/lib/languages.ts";
import { getExerciseState, getMessages } from "@/lib/db.ts";
import { exerciseStatus, localToday } from "@/lib/progress.ts";
import { threadFor, type ChatKind } from "@/lib/tutor.ts";
import { Workspace } from "@/components/Workspace";

export default async function ExercisePage(props: PageProps<"/exercises/[id]">) {
  await connection();
  const { id } = await props.params;
  const ex = getExercise(id);
  if (!ex) notFound();
  const topic = getTopic(ex.topicId)!;
  const state = getExerciseState(id);
  const language = currentLanguage(ex);
  const starter = ex.languages[language]!.starter;
  const starters = Object.fromEntries(Object.entries(ex.languages).map(([l, v]) => [l, v.starter])) as Record<Language, string>;
  const languageOptions = (Object.keys(ex.languages) as Language[]).map((l) => ({ id: l, label: LANGUAGES[l].label, note: LANGUAGES[l].note, editorFile: LANGUAGES[l].editorFile, monaco: LANGUAGES[l].monaco }));
  const thread = (kind: ChatKind) => getMessages(threadFor(kind, id)).map((m) => ({ role: m.role, content: m.content, provider: m.provider }));
  const siblings = topic.exerciseIds;
  const next = siblings[siblings.indexOf(id) + 1];

  return (
    <Workspace
      exercise={{ id: ex.id, title: ex.title, difficulty: ex.difficulty, body: ex.body, hintCount: ex.hints.length, starter, starters }}
      language={language}
      languageOptions={languageOptions}
      topic={{ id: topic.id, title: topic.title }}
      nextExerciseId={next ?? null}
      initial={{
        code: state?.code ?? starter,
        planDone: !!state?.plan_done_at,
        planText: state?.plan_text ?? null,
        planChat: thread("plan"),
        hints: ex.hints.slice(0, state?.hints_shown ?? 0),
        status: exerciseStatus(state, localToday()),
        retryDue: state?.retry_due ?? null,
        workedExample: thread("worked")[0]?.content ?? null,
        exerciseChat: thread("exercise"),
        explainChat: thread("explain"),
      }}
    />
  );
}
