import java.lang.reflect.RecordComponent;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
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

    public static void main(String[] args) {
        check("starts at 0 and steps by 1 by default", () -> {
            Solution.Counter c = Solution.makeCounter();
            return List.of(c.value().get(), c.increment().get(), c.increment().get(), c.decrement().get(), c.value().get());
        }, List.of(0, 1, 2, 1, 1));
        check("uses a custom start and step", () -> {
            Solution.Counter c = Solution.makeCounter(100, 10);
            return List.of(c.increment().get(), c.decrement().get(), c.decrement().get());
        }, List.of(110, 100, 90));
        check("reset goes back to the start, not to 0", () -> {
            Solution.Counter c = Solution.makeCounter(5);
            c.increment().get();
            c.increment().get();
            return List.of(c.reset().get(), c.value().get());
        }, List.of(5, 5));
        check("value does not change the count", () -> {
            Solution.Counter c = Solution.makeCounter(3);
            c.value().get();
            c.value().get();
            return c.increment().get();
        }, 4);
        check("counters are independent", () -> {
            Solution.Counter a = Solution.makeCounter();
            Solution.Counter b = Solution.makeCounter();
            a.increment().get();
            a.increment().get();
            return List.of(b.increment().get(), a.value().get());
        }, List.of(1, 2));
        check("functions still work when taken off the object", () -> {
            Solution.Counter c = Solution.makeCounter();
            Supplier<Integer> inc = c.increment();
            Supplier<Integer> read = c.value();
            inc.get();
            inc.get();
            return read.get();
        }, 2);
        check("the count is private",
            () -> Arrays.stream(Solution.Counter.class.getRecordComponents()).map(RecordComponent::getName).sorted().toList(),
            List.of("decrement", "increment", "reset", "value"));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
