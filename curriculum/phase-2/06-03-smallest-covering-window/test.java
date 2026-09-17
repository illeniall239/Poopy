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

    static String window(String s, String t) {
        return "<" + Solution.smallestCoveringWindow(s, t) + ">";
    }

    public static void main(String[] args) {
        check("classic example", () -> window("ADOBECODEBANC", "ABC"), "<BANC>");
        check("characters may appear in any order", () -> window("abzcxcba", "abc") + window("bba", "ab"), "<cba><ba>");
        check("leftmost of equally short windows", () -> window("acbxbca", "abc"), "<acb>");
        check("repeats in t must be covered", () -> window("aa", "aa") + window("a", "aa") + window("abcaba", "aab"), "<aa><><aba>");
        check("whole string is the only window", () -> window("a", "a") + window("xyz", "zyx"), "<a><xyz>");
        check("empty t or empty s gives an empty string", () -> window("abc", "") + window("", "a") + window("", ""), "<><><>");
        check("no window at all", () -> window("abc", "d") + window("ABC", "abc"), "<><>");
        check("400000 characters with the window at the end in O(n)", () -> {
            int n = 400000;
            String s = "a".repeat(n - 1) + "b";
            return window(s, "ab");
        }, "<ab>");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
