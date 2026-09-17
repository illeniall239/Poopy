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

    static int longest(String s) {
        return Solution.longestUniqueSubstring(s);
    }

    public static void main(String[] args) {
        check("repeating pattern", () -> longest("abcabcbb"), 3);
        check("one repeated character", () -> longest("bbbbb"), 1);
        check("substring must be contiguous", () -> longest("pwwkew") * 10 + longest("dvdf"), 33);
        check("left edge never moves backwards", () -> longest("abba") * 10 + longest("tmmzuxt"), 25);
        check("all characters distinct", () -> longest("abcdef") * 10 + longest("x"), 61);
        check("empty string gives 0", () -> longest(""), 0);
        check("spaces, digits and non-ASCII characters count as characters",
            () -> longest("a b a") * 100 + longest("1231") * 10 + longest("ñañb"), 333);
        check("100000 characters over a large alphabet in O(n)", () -> {
            int m = 50000;
            StringBuilder distinct = new StringBuilder();
            for (int i = 0; i < m; i++) distinct.append((char) (0x100 + i));
            return longest(distinct.toString() + distinct);
        }, 50000);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
