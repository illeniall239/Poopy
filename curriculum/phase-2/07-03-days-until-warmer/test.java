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
            System.out.println("FAIL - " + name + "\n    expected: " + Arrays.deepToString(new Object[] { expected }) + "\n    got:      " + Arrays.deepToString(new Object[] { value }));
        }
    }

    public static void main(String[] args) {
        check("mixed week", () -> Solution.daysUntilWarmer(new int[] { 73, 74, 75, 71, 69, 72, 76, 73 }), new int[] { 1, 1, 4, 2, 1, 1, 0, 0 });
        check("rising temperatures", () -> Solution.daysUntilWarmer(new int[] { 30, 40, 50, 60 }), new int[] { 1, 1, 1, 0 });
        check("falling temperatures never get warmer", () -> Solution.daysUntilWarmer(new int[] { 60, 50, 40 }), new int[] { 0, 0, 0 });
        check("equal temperature is not warmer", () -> new int[][] { Solution.daysUntilWarmer(new int[] { 5, 5, 6 }), Solution.daysUntilWarmer(new int[] { 7, 7, 7 }) },
            new int[][] { { 2, 1, 0 }, { 0, 0, 0 } });
        check("empty and single day", () -> new int[][] { Solution.daysUntilWarmer(new int[] {}), Solution.daysUntilWarmer(new int[] { -3 }) },
            new int[][] { {}, { 0 } });
        check("negative temperatures", () -> Solution.daysUntilWarmer(new int[] { -10, -20, -5, -30, 0 }), new int[] { 2, 1, 2, 1, 0 });
        check("does not change the input", () -> {
            int[] temps = { 3, 1, 2 };
            Solution.daysUntilWarmer(temps);
            return temps;
        }, new int[] { 3, 1, 2 });
        check("1000000 days in O(n)", () -> {
            int n = 1000000;
            int[] temps = new int[n];
            int[] expected = new int[n];
            for (int i = 0; i < n - 1; i++) {
                temps[i] = n - i;
                expected[i] = n - 1 - i;
            }
            temps[n - 1] = n + 1;
            return Arrays.equals(Solution.daysUntilWarmer(temps), expected);
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
