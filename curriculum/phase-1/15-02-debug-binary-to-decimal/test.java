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
        check("zero", () -> List.of(Solution.binaryToDecimal("0"), Solution.binaryToDecimal("0000")), List.of(0L, 0L));
        check("leading zeros are allowed", () -> Solution.binaryToDecimal("0110"), 6L);
        check("one", () -> Solution.binaryToDecimal("1"), 1L);
        check("leftmost 1 is counted", () -> List.of(Solution.binaryToDecimal("10"), Solution.binaryToDecimal("1011")), List.of(2L, 11L));
        check("all ones",
            () -> List.of(Solution.binaryToDecimal("11111111"), Solution.binaryToDecimal("1".repeat(32))),
            List.of(255L, 4294967295L));
        check("empty string is rejected", () -> thrown(() -> Solution.binaryToDecimal("")), "IllegalArgumentException: Binary string is empty");
        check("non-binary characters are rejected",
            () -> List.of(thrown(() -> Solution.binaryToDecimal("102")), thrown(() -> Solution.binaryToDecimal(" 1"))),
            List.of("IllegalArgumentException: Not a binary string: \"102\"", "IllegalArgumentException: Not a binary string: \" 1\""));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
