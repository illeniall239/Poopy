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
        check("shift by one", () -> Solution.caesarShift("abc", 1), "bcd");
        check("wraps past z", () -> Solution.caesarShift("xyz", 3), "abc");
        check("keeps case and non-letters", () -> Solution.caesarShift("Hello, World!", 5), "Mjqqt, Btwqi!");
        check("uppercase wraps within uppercase", () -> Solution.caesarShift("XYZ", 2), "ZAB");
        check("negative shift wraps backwards", () -> Solution.caesarShift("bcd", -1), "abc");
        check("negative shift wraps backwards in both cases", () -> Solution.caesarShift("aB", -1), "zA");
        check("shift of 27 behaves like 1", () -> Solution.caesarShift("abc", 27), "bcd");
        check("shift of 26 changes nothing", () -> Solution.caesarShift("abc", 26), "abc");
        check("shift of -27 behaves like -1", () -> Solution.caesarShift("a", -27), "z");
        check("huge shift behaves like its remainder", () -> Solution.caesarShift("Hi", 1000000).equals(Solution.caesarShift("Hi", 1000000 % 26)), true);
        check("digits and spaces unchanged", () -> Solution.caesarShift("route 66", 1), "spvuf 66");
        check("empty string stays empty", () -> Solution.caesarShift("", 5), "");
        check("shifting back undoes the shift", () -> Solution.caesarShift(Solution.caesarShift("Meet at 9pm, Zoe!", 11), -11), "Meet at 9pm, Zoe!");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
