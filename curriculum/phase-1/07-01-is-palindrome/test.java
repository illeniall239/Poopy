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
        check("simple lowercase palindrome", () -> Solution.isPalindrome("racecar"), true);
        check("sentence with spaces and punctuation", () -> Solution.isPalindrome("A man, a plan, a canal: Panama!"), true);
        check("not a palindrome", () -> Solution.isPalindrome("hello"), false);
        check("case is ignored (Aa)", () -> Solution.isPalindrome("Aa"), true);
        check("case is ignored (Nixon)", () -> Solution.isPalindrome("No 'x' in Nixon"), true);
        check("digits are ignored (Ab1a)", () -> Solution.isPalindrome("Ab1a"), true);
        check("digits are ignored (a12b)", () -> Solution.isPalindrome("a12b"), false);
        check("empty string is a palindrome", () -> Solution.isPalindrome(""), true);
        check("no letters is a palindrome", () -> Solution.isPalindrome("?! 42"), true);
        check("almost a palindrome fails in the middle", () -> Solution.isPalindrome("abcxba"), false);
        check("even length", () -> Solution.isPalindrome("abba"), true);
        check("odd length", () -> Solution.isPalindrome("abcba"), true);
        check("two different letters", () -> Solution.isPalindrome("ab"), false);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
