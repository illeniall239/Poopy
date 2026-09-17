import { notFound } from "next/navigation";
import { connection } from "next/server";
import { getTopic } from "@/lib/curriculum.ts";
import { allReviews, getMessages } from "@/lib/db.ts";
import { localToday } from "@/lib/progress.ts";
import { ReviewCard } from "@/components/ReviewCard";

export default async function ReviewPage(props: PageProps<"/review/[topicId]">) {
  await connection();
  const { topicId } = await props.params;
  const topic = getTopic(topicId);
  if (!topic) notFound();
  const review = allReviews().find((r) => r.topic_id === topicId);
  const today = localToday();
  const thread = getMessages(`review:${topicId}:${today}`);

  return (
    <main className="grid content-start gap-6 px-6 py-8 xl:px-10">
      <header className="grid gap-1">
        <p className="eyebrow">Spaced Review · Topic {topic.id}</p>
        <h1 className="font-display text-4xl font-bold text-balance">{topic.title}</h1>
      </header>
      {!review ? (
        <p className="text-muted">This topic isn&apos;t learned yet, so it has no Spaced Review.</p>
      ) : (
        <ReviewCard
          topicId={topicId}
          alreadyDone={review.last_done === today}
          question={thread.find((m) => m.role === "tutor")?.content ?? null}
          answer={thread.find((m) => m.role === "learner")?.content ?? null}
          result={thread.filter((m) => m.role === "tutor")[1]?.content ?? null}
          nextDue={review.due_date}
        />
      )}
    </main>
  );
}
