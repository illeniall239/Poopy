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
            String shown = String.valueOf(value);
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + (shown.length() > 300 ? shown.substring(0, 300) + "..." : shown));
        }
    }

    static String triplets(int... values) {
        return String.valueOf(Solution.zeroSumTriplets(values));
    }

    public static void main(String[] args) {
        check("two triplets in lexicographic order", () -> triplets(-1, 0, 1, 2, -1, -4), "[[-1, -1, 2], [-1, 0, 1]]");
        check("all zeros give one triplet", () -> triplets(0, 0, 0) + triplets(0, 0, 0, 0), "[[0, 0, 0]][[0, 0, 0]]");
        check("a repeated value may be used twice in one triplet", () -> triplets(-2, 0, 1, 1, 2), "[[-2, 0, 2], [-2, 1, 1]]");
        check("duplicates of the first value don't repeat a triplet", () -> triplets(3, -1, -2, -2, 4, -1, 0), "[[-2, -2, 4], [-2, -1, 3]]");
        check("no triplet gives an empty list", () -> triplets(1, 2, -2, -1) + triplets(1, 2, 3), "[][]");
        check("fewer than three values give an empty list", () -> triplets() + triplets(0) + triplets(1, -1), "[][][]");
        check("does not change the input", () -> {
            int[] values = { 2, -1, -1, 0 };
            Solution.zeroSumTriplets(values);
            return Arrays.toString(values);
        }, "[2, -1, -1, 0]");
        check("5000 values with two triplets in O(n^2)", () -> {
            int n = 5000;
            int[] values = new int[n];
            for (int i = 0; i < n - 2; i++) values[i] = i + 1;
            values[n - 2] = -3;
            values[n - 1] = -2;
            return triplets(values);
        }, "[[-3, -2, 5], [-3, 1, 2]]");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
