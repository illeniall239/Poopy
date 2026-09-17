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

    /** A nested list of Integers and Lists. */
    static List<Object> nested(Object... items) {
        return Arrays.asList(items);
    }

    public static void main(String[] args) {
        check("flattens mixed nesting in left-to-right order",
            () -> Solution.flatten(nested(1, nested(2, 3), nested(nested(4)), 5)),
            List.of(1, 2, 3, 4, 5));
        check("empty lists contribute nothing",
            () -> List.of(Solution.flatten(nested(nested(), nested(nested()), 6)), Solution.flatten(nested())),
            List.of(List.of(6), List.of()));
        check("already flat input comes back as a new equal list", () -> {
            List<Object> input = nested(3, 1, 2);
            List<Integer> result = Solution.flatten(input);
            return List.of(result, (Object) result != input);
        }, List.of(List.of(3, 1, 2), true));
        check("handles deep nesting", () -> {
            Object deep = 42;
            for (int i = 0; i < 100; i++) deep = List.of(deep);
            return Solution.flatten(nested(0, deep, 1));
        }, List.of(0, 42, 1));
        check("does not change the input", () -> {
            List<Object> input = nested(1, nested(2, nested(3)), nested());
            Solution.flatten(input);
            Solution.depth(input);
            return input;
        }, nested(1, nested(2, nested(3)), nested()));
        check("depth of flat lists is 1", () -> List.of(Solution.depth(nested(1, 2, 3)), Solution.depth(nested())), List.of(1, 1));
        check("depth takes the deepest branch",
            () -> List.of(
                Solution.depth(nested(1, nested(2, nested(3)), nested(4))),
                Solution.depth(nested(nested(4), nested(2, nested(3)))),
                Solution.depth(nested(nested(), 1))),
            List.of(3, 3, 2));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
