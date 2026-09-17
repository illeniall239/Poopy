import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public class Solution {
    /**
     * Downloads in parallel: starts every download straight away, before any has finished, and completes with the pages
     * in the same order as urls. If any download fails, the result fails with that error; the other downloads are not cancelled.
     * An empty list gives an empty list without calling fetchPage.
     */
    public static CompletableFuture<List<String>> fetchAll(List<String> urls, Function<String, CompletableFuture<String>> fetchPage) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** Downloads one after another: each starts only after the previous one completed; fails at the first failure without starting the rest. */
    public static CompletableFuture<List<String>> fetchOneByOne(List<String> urls, Function<String, CompletableFuture<String>> fetchPage) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
