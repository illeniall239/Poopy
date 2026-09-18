// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class Solution {
    public static CompletableFuture<Void> sleep(long ms) {
        return CompletableFuture.runAsync(() -> {}, CompletableFuture.delayedExecutor(ms, TimeUnit.MILLISECONDS));
    }

    public static CompletableFuture<String> withTimeout(CompletableFuture<String> promise, long ms) {
        if (ms < 0) return CompletableFuture.failedFuture(new IllegalArgumentException("ms must not be negative"));
        // copy() so the timeout settles our future, not the caller's; orTimeout cancels its timer once the future settles.
        return promise.copy().orTimeout(ms, TimeUnit.MILLISECONDS).exceptionallyCompose(error -> {
            Throwable cause = error instanceof CompletionException && error.getCause() != null ? error.getCause() : error;
            if (cause instanceof TimeoutException) {
                return CompletableFuture.failedFuture(new TimeoutException("Timed out after " + ms + "ms"));
            }
            return CompletableFuture.failedFuture(cause);
        });
    }
}
