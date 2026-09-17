import java.util.List;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable e) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + e);
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
        check("reachable with a choice of routes", () -> Solution.canReachLastIndex(new int[] {2, 3, 1, 1, 4}), true);
        check("every route lands on a zero", () -> Solution.canReachLastIndex(new int[] {3, 2, 1, 0, 4}), false);
        check("single square", () -> Solution.canReachLastIndex(new int[] {0}), true);
        check("two squares",
                () -> List.of(Solution.canReachLastIndex(new int[] {0, 1}), Solution.canReachLastIndex(new int[] {1, 0})),
                List.of(false, true));
        check("landing exactly on the last square", () -> Solution.canReachLastIndex(new int[] {2, 0, 0}), true);
        check("jumping past the end counts as reaching it", () -> Solution.canReachLastIndex(new int[] {10, 0, 0}), true);
        check("stuck before the end despite a later non-zero",
                () -> Solution.canReachLastIndex(new int[] {4, 1, 1, 0, 0, 1}), false);
        check("200000 squares reachable in O(n)", () -> {
            int n = 200000;
            int[] jumps = new int[n];
            for (int i = 0; i < n; i++) jumps[i] = n - 1 - i;
            return Solution.canReachLastIndex(jumps);
        }, true);
        check("200000 squares unreachable in O(n)", () -> {
            int n = 200000;
            int[] jumps = new int[n];
            for (int i = 0; i < n; i++) jumps[i] = Math.max(0, n - 2 - i);
            return Solution.canReachLastIndex(jumps);
        }, false);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
