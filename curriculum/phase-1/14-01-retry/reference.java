// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

public class Solution {
    public static CompletableFuture<String> retry(Supplier<CompletableFuture<String>> task, int maxAttempts) {
        return retry(task, maxAttempts, 0);
    }

    private static CompletableFuture<Void> delay(long ms) {
        return CompletableFuture.runAsync(() -> {}, CompletableFuture.delayedExecutor(ms, TimeUnit.MILLISECONDS));
    }

    public static CompletableFuture<String> retry(Supplier<CompletableFuture<String>> task, int maxAttempts, long delayMs) {
        if (maxAttempts < 1) return CompletableFuture.failedFuture(new IllegalArgumentException("maxAttempts must be at least 1"));
        return task.get().exceptionallyCompose(error -> {
            if (maxAttempts == 1) return CompletableFuture.failedFuture(error);
            return delay(delayMs).thenCompose(ignored -> retry(task, maxAttempts - 1, delayMs));
        });
    }
}
