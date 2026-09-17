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
        check("zero seconds pads every part", () -> Solution.toClock(0), "00:00:00");
        check("seconds only", () -> Solution.toClock(59), "00:00:59");
        check("exactly one minute", () -> Solution.toClock(60), "00:01:00");
        check("one second before an hour", () -> Solution.toClock(3599), "00:59:59");
        check("exactly one hour", () -> Solution.toClock(3600), "01:00:00");
        check("every part has two different digits", () -> Solution.toClock(45296), "12:34:56");
        check("single-digit parts get a leading zero", () -> Solution.toClock(3725), "01:02:05");
        check("hours do not wrap at 24", () -> Solution.toClock(90000), "25:00:00");
        check("largest allowed value", () -> Solution.toClock(359999), "99:59:59");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
