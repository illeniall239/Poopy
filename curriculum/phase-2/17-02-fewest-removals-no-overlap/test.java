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
        check("one interval overlaps two others",
                () -> Solution.fewestRemovals(new int[][] {{1, 2}, {2, 3}, {3, 4}, {1, 3}}), 1);
        check("identical intervals overlap each other",
                () -> Solution.fewestRemovals(new int[][] {{1, 2}, {1, 2}, {1, 2}}), 2);
        check("touching intervals do not overlap", () -> Solution.fewestRemovals(new int[][] {{1, 2}, {2, 3}}), 0);
        check("one long interval covering several short ones",
                () -> Solution.fewestRemovals(new int[][] {{1, 10}, {2, 3}, {4, 5}, {6, 7}}), 1);
        check("empty array and single interval",
                () -> List.of(Solution.fewestRemovals(new int[][] {}), Solution.fewestRemovals(new int[][] {{5, 9}})),
                List.of(0, 0));
        check("negative coordinates",
                () -> Solution.fewestRemovals(new int[][] {{-5, -1}, {-3, 2}, {0, 4}, {3, 6}}), 2);
        check("nested intervals",
                () -> Solution.fewestRemovals(new int[][] {{1, 100}, {2, 50}, {3, 25}, {4, 10}}), 3);
        check("unsorted input is not changed", () -> {
            int[][] intervals = {{3, 4}, {1, 2}, {2, 3}};
            int result = Solution.fewestRemovals(intervals);
            return List.of(result, Arrays.deepToString(intervals));
        }, List.of(0, "[[3, 4], [1, 2], [2, 3]]"));
        check("200000 intervals in O(n log n)", () -> {
            int K = 100000;
            int[][] intervals = new int[2 * K][];
            for (int i = 0; i < 2 * K; i++) {
                int idx = (int) ((i * 7919L) % (2 * K));
                int k = idx >> 1;
                intervals[i] = idx % 2 == 0 ? new int[] {2 * k, 2 * k + 2} : new int[] {2 * k + 1, 2 * k + 3};
            }
            return Solution.fewestRemovals(intervals);
        }, 100000);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
