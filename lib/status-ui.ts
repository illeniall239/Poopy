import type { ExerciseStatus } from "./progress.ts";

// Colour of the little status dot for an Exercise. Safe to import from client components.
export const dotClass: Record<ExerciseStatus, string> = {
  new: "bg-line",
  in_progress: "bg-warn",
  needs_explain: "bg-warn",
  waiting_retry: "bg-muted",
  retry_due: "bg-bad",
  done: "bg-accent",
};
