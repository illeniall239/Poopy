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
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + actual);
        }
    }

    public static void main(String[] args) {
        check("does not slide back on the last day", () -> Solution.daysToEscape(10, 3, 2), 8);
        check("reaching exactly the top counts as out", () -> Solution.daysToEscape(5, 3, 1), 2);
        check("one more metre needs one more day", () -> Solution.daysToEscape(6, 3, 1), 3);
        check("out on day 1 when one climb is enough", () -> Solution.daysToEscape(3, 5, 1), 1);
        check("never escapes when the slide undoes the climb", () -> Solution.daysToEscape(10, 2, 2), -1);
        check("escapes on day 1 even if the slide equals the climb", () -> Solution.daysToEscape(5, 5, 5), 1);
        check("never escapes when the slide is bigger than the climb", () -> Solution.daysToEscape(10, 3, 7), -1);
        check("no slide at all", () -> Solution.daysToEscape(10, 3, 0), 4);
        check("deep well, slow progress", () -> Solution.daysToEscape(1000000, 2, 1), 999999);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
