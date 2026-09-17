import java.util.Arrays;
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
        check("several ranges, including one starting at index 0",
            () -> Arrays.toString(Solution.rangeSums(new int[] { 3, -2, 5, 1, 4 }, new int[][] { { 0, 2 }, { 1, 3 }, { 2, 4 } })), "[6, 4, 10]");
        check("a single-element range and the whole array",
            () -> Arrays.toString(Solution.rangeSums(new int[] { 3, -2, 5, 1, 4 }, new int[][] { { 3, 3 }, { 0, 4 } })), "[1, 11]");
        check("no queries gives an empty result",
            () -> Arrays.toString(Solution.rangeSums(new int[] { 7 }, new int[][] {})), "[]");
        check("all negative values",
            () -> Arrays.toString(Solution.rangeSums(new int[] { -4, -6, -1 }, new int[][] { { 0, 1 }, { 1, 2 }, { 0, 0 } })), "[-10, -7, -4]");
        check("answers stay in query order, repeats included",
            () -> Arrays.toString(Solution.rangeSums(new int[] { 2, 9, 4 }, new int[][] { { 2, 2 }, { 0, 0 }, { 2, 2 }, { 0, 2 } })), "[4, 2, 4, 15]");
        check("does not change the inputs", () -> {
            int[] values = { 1, 2, 3 };
            int[][] queries = { { 0, 2 } };
            Solution.rangeSums(values, queries);
            return Arrays.toString(values) + " " + Arrays.deepToString(queries);
        }, "[1, 2, 3] [[0, 2]]");
        check("1000000 long queries over 1000000 values in O(n + q)", () -> {
            int n = 1000000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = i;
            int[][] queries = new int[n][];
            long[] expected = new long[n];
            for (int q = 0; q < n; q++) {
                int i = q % (n / 2);
                int j = n - 1 - i;
                queries[q] = new int[] { i, j };
                expected[q] = (long) (i + j) * (j - i + 1) / 2;
            }
            return Arrays.equals(Solution.rangeSums(values, queries), expected);
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
