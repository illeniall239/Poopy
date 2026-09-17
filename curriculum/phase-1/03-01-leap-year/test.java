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
        check("divisible by 4 is a leap year", () -> Solution.isLeapYear(2024), true);
        check("not divisible by 4 is not a leap year", () -> Solution.isLeapYear(2023), false);
        check("divisible by 100 but not 400 is not a leap year (1900)", () -> Solution.isLeapYear(1900), false);
        check("divisible by 100 but not 400 is not a leap year (2100)", () -> Solution.isLeapYear(2100), false);
        check("divisible by 400 is a leap year (2000)", () -> Solution.isLeapYear(2000), true);
        check("divisible by 400 is a leap year (2400)", () -> Solution.isLeapYear(2400), true);
        check("even but not divisible by 4", () -> Solution.isLeapYear(2022), false);
        check("small years follow the same rules (4)", () -> Solution.isLeapYear(4), true);
        check("small years follow the same rules (1)", () -> Solution.isLeapYear(1), false);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
