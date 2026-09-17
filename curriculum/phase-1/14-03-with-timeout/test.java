import java.util.List;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw:    " + t);
            return;
        }
        if (Objects.deepEquals(value, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + value);
        }
    }

    /** Waits for the future; returns the exception it failed with, or null if it succeeded. */
    static Throwable failure(CompletableFuture<?> future) {
        try {
            future.join();
            return null;
        } catch (CompletionException e) {
            return e.getCause() != null ? e.getCause() : e;
        }
    }

    /** "ExceptionType: message" of the failure, or "no exception". */
    static String describe(Throwable error) {
        return error == null ? "no exception" : error.getClass().getSimpleName() + ": " + error.getMessage();
    }

    public static void main(String[] args) {
        check("sleep completes with null after the delay", () -> {
            long started = System.currentTimeMillis();
            Object result = Solution.sleep(20).join();
            return List.of(result == null, System.currentTimeMillis() - started >= 15);
        }, List.of(true, true));
        check("completes with the value when the promise is fast enough",
            () -> Solution.withTimeout(Solution.sleep(5).thenApply(v -> "done"), 50).join(),
            "done");
        check("fails with a timeout error when the promise is too slow",
            () -> describe(failure(Solution.withTimeout(Solution.sleep(50).thenApply(v -> "late"), 10))),
            "TimeoutException: Timed out after 10ms");
        check("does not wait for the slow promise after timing out", () -> {
            long started = System.currentTimeMillis();
            Throwable error = failure(Solution.withTimeout(Solution.sleep(300).thenApply(v -> "late"), 10));
            return List.of(error != null, System.currentTimeMillis() - started < 200);
        }, List.of(true, true));
        check("passes through the original failure", () -> {
            RuntimeException boom = new RuntimeException("boom");
            return failure(Solution.withTimeout(CompletableFuture.failedFuture(boom), 50)) == boom;
        }, true);
        check("an already-completed promise wins even with a 0ms timeout",
            () -> Solution.withTimeout(CompletableFuture.completedFuture("ready"), 0).join(),
            "ready");
        check("a late failure after the timeout is ignored", () -> {
            CompletableFuture<String> late = Solution.sleep(20).<String>thenApply(v -> {
                throw new RuntimeException("late failure");
            });
            String result = describe(failure(Solution.withTimeout(late, 5)));
            Solution.sleep(40).join();
            return result;
        }, "TimeoutException: Timed out after 5ms");
        check("negative ms fails with an IllegalArgumentException",
            () -> describe(failure(Solution.withTimeout(CompletableFuture.completedFuture("x"), -1))),
            "IllegalArgumentException: ms must not be negative");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
