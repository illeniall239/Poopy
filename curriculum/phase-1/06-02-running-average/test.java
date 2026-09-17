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
        check("increasing numbers", () -> Solution.runningAverages(new double[]{1, 2, 3, 4}), new double[]{1, 1.5, 2, 2.5});
        check("negative numbers pull the average down", () -> Solution.runningAverages(new double[]{10, -10, 6}), new double[]{10, 0, 2});
        check("single element", () -> Solution.runningAverages(new double[]{5}), new double[]{5});
        check("empty array gives empty array", () -> Solution.runningAverages(new double[]{}), new double[]{});
        check("constant values keep a constant average", () -> Solution.runningAverages(new double[]{4, 4, 4, 4}), new double[]{4, 4, 4, 4});
        check("first element is its own average (divide by count so far)", () -> Solution.runningAverages(new double[]{8, 0, 0, 0}), new double[]{8, 4, 8.0 / 3, 2});
        check("does not modify the input", () -> {
            double[] nums = {3, 5, 7};
            Solution.runningAverages(nums);
            return nums;
        }, new double[]{3, 5, 7});
        check("returns a new array, not the input", () -> {
            double[] nums = {3, 5, 7};
            return Solution.runningAverages(nums) != nums;
        }, true);
        check("large input", () -> {
            double[] nums = new double[100000];
            for (int i = 0; i < nums.length; i++) nums[i] = 2;
            double[] result = Solution.runningAverages(nums);
            return new double[]{result.length, result[99999]};
        }, new double[]{100000, 2});
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
