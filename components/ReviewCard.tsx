"use client";
import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import { Markdown } from "./Markdown";
import { answerReview, getReviewQuestion } from "@/app/actions";

type Props = { topicId: string; alreadyDone: boolean; question: string | null; answer: string | null; result: string | null; nextDue: string };

export function ReviewCard({ topicId, alreadyDone, question: initialQuestion, answer: initialAnswer, result: initialResult, nextDue: initialNextDue }: Props) {
  const [question, setQuestion] = useState(initialQuestion);
  const [answer, setAnswer] = useState(initialAnswer ?? "");
  const [result, setResult] = useState<string | null>(alreadyDone ? initialResult : null);
  const [nextDue, setNextDue] = useState(initialNextDue);
  const [error, setError] = useState<string | null>(null);
  const [pending, start] = useTransition();

  useEffect(() => {
    if (question || alreadyDone) return;
    start(async () => {
      try {
        setQuestion(await getReviewQuestion(topicId));
      } catch (e) {
        setError((e as Error).message);
      }
    });
  }, [question, alreadyDone, topicId]);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!answer.trim()) return;
    start(async () => {
      try {
        const r = await answerReview(topicId, answer.trim());
        setResult(`**${r.passed ? "Passed" : "Not yet"}.** ${r.feedback}`);
        setNextDue(r.nextDue);
      } catch (e) {
        setError((e as Error).message);
      }
    });
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <section className="panel grid content-start gap-3 p-6">
        <p className="eyebrow">Question</p>
        {question ? <Markdown text={question} className="text-base" /> : <p className="animate-pulse text-muted">{pending ? "Writing today's question…" : ""}</p>}
      </section>

      <section className="panel grid content-start gap-4 p-6">
        <form onSubmit={submit} className="grid gap-3">
          <label htmlFor="review-answer" className="eyebrow">Your answer</label>
          <textarea
            id="review-answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={9}
            disabled={!question || !!result}
            className="field"
            placeholder="Answer in a few sentences, in your own words."
          />
          {!result && (
            <button type="submit" disabled={pending || !question || !answer.trim()} className="btn btn-primary justify-self-start">
              {pending && question ? "Checking…" : "Submit answer"}
            </button>
          )}
        </form>
        {error && <p className="rounded bg-bad-soft px-3 py-2 text-sm" role="alert">{error}</p>}
        {result && (
          <div className="grid gap-2 rounded-md bg-accent-soft p-4">
            <Markdown text={result} />
            <p className="text-sm text-muted">Next review of this topic: {nextDue}.</p>
            <Link href="/" className="btn justify-self-start">Back to Today</Link>
          </div>
        )}
      </section>
    </div>
  );
}
