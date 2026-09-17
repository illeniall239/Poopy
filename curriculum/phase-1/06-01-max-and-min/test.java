import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object actual;
        try {
            actual = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + t);
            return;
        }
        if (Objects.deepEquals(actual, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + show(expected) + "\n    got:      " + show(actual));
        }
    }

    static String show(Object o) {
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }

    public static void main(String[] args) {
        check("mixed positive numbers", () -> Solution.maxAndMin(new double[]{3, 9, 1, 4}), new Solution.MaxMin(9, 1));
        check("all negative numbers (max is not 0)", () -> Solution.maxAndMin(new double[]{-5, -2, -8}), new Solution.MaxMin(-2, -8));
        check("all positive numbers (min is not 0)", () -> Solution.maxAndMin(new double[]{12, 40, 7, 30}), new Solution.MaxMin(40, 7));
        check("single element is both max and min", () -> Solution.maxAndMin(new double[]{7}), new Solution.MaxMin(7, 7));
        check("empty array returns null", () -> Solution.maxAndMin(new double[]{}), null);
        check("max first and min last", () -> Solution.maxAndMin(new double[]{100, 50, 0, -50}), new Solution.MaxMin(100, -50));
        check("decimals and repeated values", () -> Solution.maxAndMin(new double[]{2.5, 2.5, -0.5, 2.5}), new Solution.MaxMin(2.5, -0.5));
        check("does not modify the input", () -> {
            double[] nums = {4, 1, 3};
            Solution.maxAndMin(nums);
            return nums;
        }, new double[]{4, 1, 3});
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
