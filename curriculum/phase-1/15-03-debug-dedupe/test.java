import java.util.ArrayList;
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

    /** A mutable list, so a solution that changes its input shows up as a wrong result rather than an exception. */
    static List<Integer> list(Integer... items) {
        return new ArrayList<>(List.of(items));
    }

    public static void main(String[] args) {
        check("removes scattered duplicates, keeping first appearances", () -> Solution.dedupe(list(1, 2, 1, 3, 2)), List.of(1, 2, 3));
        check("removes runs of the same number",
            () -> List.of(Solution.dedupe(list(5, 5, 5, 5)), Solution.dedupe(list(1, 1, 2, 2, 2, 3))),
            List.of(List.of(5), List.of(1, 2, 3)));
        check("empty list", () -> Solution.dedupe(list()), List.of());
        check("does not change the input", () -> {
            List<Integer> input = list(4, 4, 7);
            List<Integer> result = Solution.dedupe(input);
            return List.of(result, input);
        }, List.of(List.of(4, 7), List.of(4, 4, 7)));
        check("returns a new list even without duplicates", () -> {
            List<Integer> input = list(3, 1, 2);
            List<Integer> result = Solution.dedupe(input);
            return List.of(result, result != input);
        }, List.of(List.of(3, 1, 2), true));
        check("keeps the position of each first appearance", () -> Solution.dedupe(list(2, 9, 2, 9, 0, 2)), List.of(2, 9, 0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
