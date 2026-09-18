// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function retry(task: () => Promise<string>, maxAttempts: number, delayMs: number = 0): Promise<string> {
  if (maxAttempts < 1) throw new RangeError("maxAttempts must be at least 1");
  let lastError: unknown;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await task();
    } catch (error) {
      lastError = error;
      if (attempt < maxAttempts) await wait(delayMs);
    }
  }
  throw lastError;
}
