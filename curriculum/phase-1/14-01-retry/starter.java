import java.util.concurrent.CompletableFuture;
import java.util.function.Supplier;

public class Solution {
    /** Same as retry(task, maxAttempts, 0). */
    public static CompletableFuture<String> retry(Supplier<CompletableFuture<String>> task, int maxAttempts) {
        return retry(task, maxAttempts, 0);
    }

    /**
     * Calls task (each call is one attempt) up to maxAttempts times, never overlapping, waiting delayMs between attempts.
     * Completes with the first successful value, or fails with the last attempt's error (the same exception object).
     * maxAttempts below 1 gives a future that fails with IllegalArgumentException("maxAttempts must be at least 1") without calling task.
     */
    public static CompletableFuture<String> retry(Supplier<CompletableFuture<String>> task, int maxAttempts, long delayMs) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
