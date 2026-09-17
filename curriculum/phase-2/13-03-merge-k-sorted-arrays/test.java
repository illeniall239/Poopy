import java.util.Arrays;
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
            System.out.println("FAIL - " + name + "\n    expected: " + Arrays.deepToString(new Object[] {expected})
                    + "\n    got:      " + Arrays.deepToString(new Object[] {value}));
        }
    }

    public static void main(String[] args) {
        check("three interleaving arrays",
                () -> Solution.mergeKSorted(new int[][] {{1, 4, 7}, {2, 5, 8}, {3, 6, 9}}),
                new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9});
        check("empty inner arrays and duplicates",
                () -> Solution.mergeKSorted(new int[][] {{}, {1, 1, 3}, {}, {1, 2}}),
                new int[] {1, 1, 1, 2, 3});
        check("no arrays at all", () -> Solution.mergeKSorted(new int[][] {}), new int[] {});
        check("a single array", () -> Solution.mergeKSorted(new int[][] {{-3, 0, 2}}), new int[] {-3, 0, 2});
        check("negatives and different lengths",
                () -> Solution.mergeKSorted(new int[][] {{-10, -5, 0, 5}, {-7}, {1, 2, 3, 4, 100}}),
                new int[] {-10, -7, -5, 0, 1, 2, 3, 4, 5, 100});
        check("does not change the input arrays", () -> {
            int[][] input = {{1, 3}, {2, 4}};
            Solution.mergeKSorted(input);
            return input;
        }, new int[][] {{1, 3}, {2, 4}});
        check("10 000 arrays of 20 values, O(N log k)", () -> {
            int k = 10000, m = 20;
            int[][] arrays = new int[k][m];
            for (int j = 0; j < k; j++)
                for (int i = 0; i < m; i++) arrays[j][i] = i * k + j;
            int[] result = Solution.mergeKSorted(arrays);
            if (result.length != k * m) return false;
            for (int i = 0; i < result.length; i++) if (result[i] != i) return false;
            return true;
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
