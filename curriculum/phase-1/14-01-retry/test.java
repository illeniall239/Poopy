import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.atomic.AtomicInteger;
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

    static void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
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

    /** A task that fails `failures` times (with a new exception each time), then completes with "ok". */
    static class Flaky {
        final int failures;
        final List<Throwable> errors = Collections.synchronizedList(new ArrayList<>());

        Flaky(int failures) {
            this.failures = failures;
        }

        CompletableFuture<String> task() {
            return CompletableFuture.supplyAsync(() -> {
                sleep(1);
                if (errors.size() < failures) {
                    RuntimeException error = new RuntimeException("failure " + (errors.size() + 1));
                    errors.add(error);
                    throw error;
                }
                return "ok";
            });
        }
    }

    public static void main(String[] args) {
        check("resolves on the first try without retrying", () -> {
            AtomicInteger calls = new AtomicInteger();
            String result = Solution.retry(() -> {
                calls.incrementAndGet();
                return CompletableFuture.completedFuture("first");
            }, 5).join();
            return List.of(result, calls.get());
        }, List.of("first", 1));
        check("retries after failures until one succeeds", () -> {
            Flaky flaky = new Flaky(2);
            return List.of(Solution.retry(flaky::task, 3).join(), flaky.errors.size());
        }, List.of("ok", 2));
        check("fails with the last attempt's error when every attempt fails", () -> {
            Flaky flaky = new Flaky(10);
            Throwable error = failure(Solution.retry(flaky::task, 3));
            return List.of(error == flaky.errors.get(2), flaky.errors.size());
        }, List.of(true, 3));
        check("one attempt means no retries", () -> {
            Flaky flaky = new Flaky(1);
            return List.of(failure(Solution.retry(flaky::task, 1)).getMessage(), flaky.errors.size());
        }, List.of("failure 1", 1));
        check("maxAttempts below 1 fails with an IllegalArgumentException and never calls the task", () -> {
            AtomicInteger calls = new AtomicInteger();
            Supplier<CompletableFuture<String>> task = () -> {
                calls.incrementAndGet();
                return CompletableFuture.completedFuture("x");
            };
            Throwable zero = failure(Solution.retry(task, 0));
            Throwable negative = failure(Solution.retry(task, -2));
            return List.of(zero instanceof IllegalArgumentException, zero.getMessage(), negative instanceof IllegalArgumentException, calls.get());
        }, List.of(true, "maxAttempts must be at least 1", true, 0));
        check("attempts never overlap", () -> {
            AtomicInteger running = new AtomicInteger(), maxRunning = new AtomicInteger(), calls = new AtomicInteger();
            Supplier<CompletableFuture<String>> task = () -> CompletableFuture.supplyAsync(() -> {
                maxRunning.accumulateAndGet(running.incrementAndGet(), Math::max);
                int call = calls.incrementAndGet();
                sleep(5);
                running.decrementAndGet();
                if (call < 4) throw new RuntimeException("not yet");
                return "done";
            });
            return List.of(Solution.retry(task, 4).join(), maxRunning.get());
        }, List.of("done", 1));
        check("waits delayMs between attempts", () -> {
            Flaky flaky = new Flaky(10);
            long started = System.currentTimeMillis();
            failure(Solution.retry(flaky::task, 3, 25));
            return System.currentTimeMillis() - started >= 45;
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
