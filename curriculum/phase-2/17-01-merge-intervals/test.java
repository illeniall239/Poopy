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
            String shown = String.valueOf(value);
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + (shown.length() > 300 ? shown.substring(0, 300) + "..." : shown));
        }
    }

    static String merged(int[]... intervals) {
        return Arrays.deepToString(Solution.mergeIntervals(intervals));
    }

    static int[] p(int start, int end) {
        return new int[] { start, end };
    }

    public static void main(String[] args) {
        check("merges overlapping neighbours", () -> merged(p(1, 3), p(2, 6), p(8, 10), p(15, 18)), "[[1, 6], [8, 10], [15, 18]]");
        check("touching endpoints merge", () -> merged(p(1, 4), p(4, 5)) + merged(p(1, 3), p(4, 5)), "[[1, 5]][[1, 3], [4, 5]]");
        check("unsorted input", () -> merged(p(8, 10), p(1, 3), p(2, 6)) + merged(p(5, 6), p(1, 2)), "[[1, 6], [8, 10]][[1, 2], [5, 6]]");
        check("nested intervals disappear into the outer one",
            () -> merged(p(1, 10), p(2, 3), p(4, 5)) + merged(p(2, 3), p(1, 10)), "[[1, 10]][[1, 10]]");
        check("a chain of overlaps merges into one", () -> merged(p(1, 2), p(2, 3), p(3, 4), p(4, 5)), "[[1, 5]]");
        check("negative bounds and single-point intervals",
            () -> merged(p(-5, -1), p(-2, 0), p(3, 4)) + merged(p(5, 5), p(5, 5), p(7, 7)), "[[-5, 0], [3, 4]][[5, 5], [7, 7]]");
        check("empty input and a single interval", () -> merged() + merged(p(1, 2)), "[][[1, 2]]");
        check("does not change the input or return its pairs", () -> {
            int[] first = p(4, 6);
            int[][] intervals = { first, p(1, 5), p(9, 9) };
            int[][] result = Solution.mergeIntervals(intervals);
            boolean fresh = true;
            for (int[] pair : result) for (int[] original : intervals) if (pair == original) fresh = false;
            return Arrays.deepToString(result) + Arrays.deepToString(intervals) + Arrays.toString(first) + fresh;
        }, "[[1, 6], [9, 9]][[4, 6], [1, 5], [9, 9]][4, 6]true");
        check("400000 shuffled disjoint intervals in O(n log n)", () -> {
            int n = 400000;
            int[][] intervals = new int[n][];
            for (int i = 0; i < n; i++) {
                int k = (int) (((long) i * 7919) % n);
                intervals[i] = p(3 * k, 3 * k + 1);
            }
            int[][] result = Solution.mergeIntervals(intervals);
            if (result.length != n) return "wrong length " + result.length;
            for (int i = 0; i < n; i++) if (result[i][0] != 3 * i || result[i][1] != 3 * i + 1) return "result is not sorted and disjoint at " + i;
            return "ok";
        }, "ok");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
