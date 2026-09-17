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

    /** "ExceptionType: message" of what action throws, or "no exception". */
    static String thrown(Runnable action) {
        try {
            action.run();
            return "no exception";
        } catch (Throwable t) {
            return t.getClass().getSimpleName() + ": " + t.getMessage();
        }
    }

    public static void main(String[] args) {
        check("parses a plain age", () -> Solution.parseAge("42"), 42);
        check("ignores surrounding spaces and leading zeros", () -> List.of(Solution.parseAge("  7 "), Solution.parseAge("007")), List.of(7, 7));
        check("accepts the boundaries 0 and 150", () -> List.of(Solution.parseAge("0"), Solution.parseAge("150")), List.of(0, 150));
        check("empty or blank input is reported as empty, not as 0",
            () -> List.of(thrown(() -> Solution.parseAge("")), thrown(() -> Solution.parseAge("   "))),
            List.of("IllegalArgumentException: Age is empty", "IllegalArgumentException: Age is empty"));
        check("non-digits are rejected with the original input in the message",
            () -> List.of(thrown(() -> Solution.parseAge("12.5")), thrown(() -> Solution.parseAge("abc")), thrown(() -> Solution.parseAge(" -5"))),
            List.of(
                "NumberFormatException: Age must be a whole number, got \"12.5\"",
                "NumberFormatException: Age must be a whole number, got \"abc\"",
                "NumberFormatException: Age must be a whole number, got \" -5\""));
        check("inputs that a lenient parser would accept are still rejected",
            () -> List.of(thrown(() -> Solution.parseAge("1e2")), thrown(() -> Solution.parseAge("12abc")), thrown(() -> Solution.parseAge("4 2"))),
            List.of(
                "NumberFormatException: Age must be a whole number, got \"1e2\"",
                "NumberFormatException: Age must be a whole number, got \"12abc\"",
                "NumberFormatException: Age must be a whole number, got \"4 2\""));
        check("too old is an IllegalArgumentException",
            () -> List.of(thrown(() -> Solution.parseAge("151")), thrown(() -> Solution.parseAge(" 0200"))),
            List.of(
                "IllegalArgumentException: Age must be between 0 and 150, got 151",
                "IllegalArgumentException: Age must be between 0 and 150, got 200"));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
