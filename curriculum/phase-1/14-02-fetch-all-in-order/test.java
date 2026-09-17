import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
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

    static final Map<String, Integer> delays = Map.of("a", 30, "b", 10, "c", 20, "bad", 5, "slow", 40);

    /** A fake fetchPage that records when each download starts and ends. "bad" fails. No network. */
    static class Fake {
        final List<String> log = Collections.synchronizedList(new ArrayList<>());

        CompletableFuture<String> fetchPage(String url) {
            log.add("start " + url);
            return CompletableFuture.supplyAsync(() -> {
                sleep(delays.get(url));
                log.add("end " + url);
                if (url.equals("bad")) throw new RuntimeException("download failed: bad");
                return "page " + url;
            });
        }
    }

    public static void main(String[] args) {
        check("fetchAll returns pages in input order, not finishing order", () -> {
            Fake fake = new Fake();
            return Solution.fetchAll(List.of("a", "b", "c"), fake::fetchPage).join();
        }, List.of("page a", "page b", "page c"));
        check("fetchAll starts every download before any finishes", () -> {
            Fake fake = new Fake();
            Solution.fetchAll(List.of("a", "b", "c"), fake::fetchPage).join();
            return new ArrayList<>(fake.log.subList(0, 3));
        }, List.of("start a", "start b", "start c"));
        check("fetchAll fails when a download fails, but the other downloads still finish", () -> {
            Fake fake = new Fake();
            Throwable error = failure(Solution.fetchAll(List.of("slow", "bad"), fake::fetchPage));
            sleep(60);
            return List.of(error.getMessage(), fake.log.contains("end slow"));
        }, List.of("download failed: bad", true));
        check("fetchOneByOne runs downloads strictly one after another", () -> {
            Fake fake = new Fake();
            List<String> pages = Solution.fetchOneByOne(List.of("a", "b", "c"), fake::fetchPage).join();
            return List.of(pages, new ArrayList<>(fake.log));
        }, List.of(List.of("page a", "page b", "page c"), List.of("start a", "end a", "start b", "end b", "start c", "end c")));
        check("fetchOneByOne stops at the first failure", () -> {
            Fake fake = new Fake();
            Throwable error = failure(Solution.fetchOneByOne(List.of("b", "bad", "c"), fake::fetchPage));
            sleep(30);
            return List.of(error.getMessage(), new ArrayList<>(fake.log));
        }, List.of("download failed: bad", List.of("start b", "end b", "start bad", "end bad")));
        check("empty list gives an empty list without fetching", () -> {
            Fake fake = new Fake();
            List<String> all = Solution.fetchAll(List.of(), fake::fetchPage).join();
            List<String> oneByOne = Solution.fetchOneByOne(List.of(), fake::fetchPage).join();
            return List.of(all, oneByOne, new ArrayList<>(fake.log));
        }, List.of(List.of(), List.of(), List.of()));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
