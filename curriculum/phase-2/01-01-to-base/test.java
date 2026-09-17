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
        check("ten in binary", () -> Solution.toBase(10, 2), "1010");
        check("digits come out most significant first", () -> Solution.toBase(6, 2), "110");
        check("letters for digits above 9", () -> Solution.toBase(255, 16), "ff");
        check("zero is written as a single digit", () -> Solution.toBase(0, 7), "0");
        check("largest 32-bit integer in base 16 and base 2",
            () -> Solution.toBase(2147483647, 16) + " " + Solution.toBase(2147483647, 2),
            "7fffffff " + "1".repeat(31));
        check("fromBase reads binary", () -> Solution.fromBase("1010", 2), 10);
        check("fromBase reads zero and letters",
            () -> Solution.fromBase("0", 2) + " " + Solution.fromBase("7fffffff", 16), "0 2147483647");
        check("round trip in every base", () -> {
            for (int base = 2; base <= 16; base++) {
                for (int n : new int[] { 1, 15, 16, 999, 123456789, 2147483646 }) {
                    if (Solution.fromBase(Solution.toBase(n, base), base) != n) return "failed for " + n + " in base " + base;
                }
            }
            return Solution.toBase(123456789, 10);
        }, "123456789");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
