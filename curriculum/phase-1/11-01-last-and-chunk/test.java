import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
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

    /** True when action throws an exception of the given type. */
    static boolean throwsType(Runnable action, Class<? extends Throwable> type) {
        try {
            action.run();
            return false;
        } catch (Throwable t) {
            return type.isInstance(t);
        }
    }

    public static void main(String[] args) {
        check("last returns the final element",
            () -> List.of(Solution.last(List.of(3, 1, 4)), Solution.last(List.of("a"))),
            List.of(Optional.of(4), Optional.of("a")));
        check("last of an empty list is empty", () -> Solution.last(List.of()), Optional.empty());
        check("last returns a zero final element, not empty", () -> Solution.last(List.of(1, 0)), Optional.of(0));
        check("chunk leaves a shorter final group",
            () -> Solution.chunk(List.of(1, 2, 3, 4, 5), 2),
            List.of(List.of(1, 2), List.of(3, 4), List.of(5)));
        check("chunk with size equal to length gives one group",
            () -> Solution.chunk(List.of("a", "b", "c"), 3),
            List.of(List.of("a", "b", "c")));
        check("chunk with size larger than length gives one group", () -> Solution.chunk(List.of(1, 2), 10), List.of(List.of(1, 2)));
        check("chunk of an empty list is empty", () -> Solution.chunk(List.of(), 4), List.of());
        check("chunk rejects sizes below 1",
            () -> List.of(
                throwsType(() -> Solution.chunk(List.of(1, 2), 0), IllegalArgumentException.class),
                throwsType(() -> Solution.chunk(List.of(1, 2), -1), IllegalArgumentException.class)),
            List.of(true, true));
        check("neither function changes the input", () -> {
            List<Integer> items = new ArrayList<>(List.of(1, 2, 3));
            Solution.last(items);
            Solution.chunk(items, 2);
            return items;
        }, List.of(1, 2, 3));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
