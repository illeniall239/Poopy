import { notFound } from "next/navigation";
import { connection } from "next/server";
import { getInterview, getMessages } from "@/lib/db.ts";
import { INTERVIEW_KINDS, isInterviewKind, type Feedback } from "@/lib/interview.ts";
import { LANGUAGES, isLanguage } from "@/lib/languages.ts";
import { InterviewRoom } from "@/components/InterviewRoom";

export default async function InterviewRoomPage(props: PageProps<"/interview/[id]">) {
  await connection();
  const { id } = await props.params;
  const iv = getInterview(Number(id));
  if (!iv || !isInterviewKind(iv.kind)) notFound();
  const kind = INTERVIEW_KINDS[iv.kind];
  const language = iv.language && isLanguage(iv.language) ? iv.language : "typescript";

  return (
    <InterviewRoom
      id={iv.id}
      label={kind.label}
      minutes={kind.minutes}
      editor={kind.editor}
      startedAt={iv.started_at.replace(" ", "T") + "Z"}
      language={{ monaco: LANGUAGES[language].monaco, label: LANGUAGES[language].label, file: LANGUAGES[language].editorFile }}
      initialCode={iv.code ?? ""}
      initialMessages={getMessages(`interview:${iv.id}`).map((m) => ({ role: m.role, content: m.content, provider: m.provider }))}
      initialFeedback={iv.feedback ? (JSON.parse(iv.feedback) as Feedback) : null}
    />
  );
}
