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
        check("ones place: 1", () -> Solution.toRoman(1), "I");
        check("ones place: 3", () -> Solution.toRoman(3), "III");
        check("ones place: 4", () -> Solution.toRoman(4), "IV");
        check("ones place: 5", () -> Solution.toRoman(5), "V");
        check("ones place: 8", () -> Solution.toRoman(8), "VIII");
        check("ones place: 9", () -> Solution.toRoman(9), "IX");
        check("tens and ones together", () -> Solution.toRoman(14), "XIV");
        check("tens place: 40", () -> Solution.toRoman(40), "XL");
        check("tens place: 90", () -> Solution.toRoman(90), "XC");
        check("zero digits in the middle write nothing (101)", () -> Solution.toRoman(101), "CI");
        check("zero digits in the middle write nothing (2006)", () -> Solution.toRoman(2006), "MMVI");
        check("hundreds use C, D and M (400)", () -> Solution.toRoman(400), "CD");
        check("hundreds use C, D and M (900)", () -> Solution.toRoman(900), "CM");
        check("hundreds use C, D and M (500)", () -> Solution.toRoman(500), "D");
        check("every place at once (1994)", () -> Solution.toRoman(1994), "MCMXCIV");
        check("every place at once (3888)", () -> Solution.toRoman(3888), "MMMDCCCLXXXVIII");
        check("largest allowed number", () -> Solution.toRoman(3999), "MMMCMXCIX");
        check("zero gives an empty string", () -> Solution.toRoman(0), "");
        check("negative gives an empty string", () -> Solution.toRoman(-5), "");
        check("4000 gives an empty string", () -> Solution.toRoman(4000), "");
        check("non-whole numbers give an empty string", () -> Solution.toRoman(2.5), "");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
