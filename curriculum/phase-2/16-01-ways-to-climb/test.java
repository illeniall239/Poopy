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
        check("zero steps: one way (do nothing)", () -> Solution.climbWays(0), 1L);
        check("one step", () -> Solution.climbWays(1), 1L);
        check("two steps", () -> Solution.climbWays(2), 2L);
        check("three steps", () -> Solution.climbWays(3), 3L);
        check("five steps", () -> Solution.climbWays(5), 8L);
        check("ten steps", () -> Solution.climbWays(10), 89L);
        check("45 steps needs stored sub-answers", () -> Solution.climbWays(45), 1836311903L);
        check("70 steps", () -> Solution.climbWays(70), 308061521170129L);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
