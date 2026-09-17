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

    static long area(int... heights) {
        return Solution.widestContainer(heights);
    }

    public static void main(String[] args) {
        check("classic example", () -> area(1, 8, 6, 2, 5, 4, 8, 3, 7), 49L);
        check("outer walls win despite a dip in the middle", () -> area(4, 3, 2, 1, 4), 16L);
        check("width beats height", () -> area(1, 2, 1), 2L);
        check("two tall neighbours beat wide short walls", () -> area(2, 3, 4, 5, 18, 17, 6), 17L);
        check("two walls", () -> area(1, 1) * 10 + area(3, 9), 13L);
        check("fewer than two walls give 0", () -> area() + area(5), 0L);
        check("zero-height walls hold nothing", () -> area(0, 0, 0) * 100 + area(0, 4, 0, 4, 0), 8L);
        check("does not change the input", () -> {
            int[] heights = { 3, 1, 2 };
            Solution.widestContainer(heights);
            return Arrays.toString(heights);
        }, "[3, 1, 2]");
        check("400000 alternating walls in O(n)", () -> {
            int n = 400000;
            int[] heights = new int[n];
            for (int i = 0; i < n; i++) heights[i] = i % 2 == 0 ? 1000 : 1;
            return Solution.widestContainer(heights);
        }, 1000L * (400000 - 2));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
