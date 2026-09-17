import java.util.concurrent.CompletableFuture;

public class Solution {
    /** A future that completes (with null) after ms milliseconds. */
    public static CompletableFuture<Void> sleep(long ms) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /**
     * A new future that settles like promise if promise settles within ms milliseconds (same value, or the same exception object);
     * otherwise fails with TimeoutException("Timed out after <ms>ms") without waiting for promise any longer. Whatever promise
     * does later is ignored. Negative ms gives a future that fails with IllegalArgumentException("ms must not be negative").
     */
    public static CompletableFuture<String> withTimeout(CompletableFuture<String> promise, long ms) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
