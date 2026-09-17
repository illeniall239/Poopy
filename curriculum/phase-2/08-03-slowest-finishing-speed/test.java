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

    public static void main(String[] args) {
        check("speed between the smallest and largest stack", () -> Solution.minShredSpeed(new int[] { 3, 6, 7, 11 }, 8), 4);
        check("one hour per stack needs the largest stack as speed", () -> Solution.minShredSpeed(new int[] { 30, 11, 23, 4, 20 }, 5), 30);
        check("one extra hour lowers the speed", () -> Solution.minShredSpeed(new int[] { 30, 11, 23, 4, 20 }, 6), 23);
        check("a partial last hour still counts as an hour", () -> List.of(
            Solution.minShredSpeed(new int[] { 10 }, 3), Solution.minShredSpeed(new int[] { 10 }, 5), Solution.minShredSpeed(new int[] { 10 }, 10)),
            List.of(4, 2, 1));
        check("plenty of time gives speed 1", () -> Solution.minShredSpeed(new int[] { 5, 5 }, 1000000000), 1);
        check("single one-page stack", () -> Solution.minShredSpeed(new int[] { 1 }, 1), 1);
        check("does not change the input", () -> {
            int[] stacks = { 11, 3, 7 };
            Solution.minShredSpeed(stacks, 5);
            return stacks;
        }, new int[] { 11, 3, 7 });
        check("huge stacks with the answer far from both ends, in O(n log m)", () -> {
            int n = 100000;
            int[] stacks = new int[n];
            Arrays.fill(stacks, 1);
            stacks[n / 2] = 1000000000;
            int first = Solution.minShredSpeed(stacks, n + 1);
            stacks[0] = 999999999;
            return List.of(first, Solution.minShredSpeed(stacks, n + 4));
        }, List.of(500000000, 333333334));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
