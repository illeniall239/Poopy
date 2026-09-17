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
        check("hasLowercase finds a lowercase letter", () -> Solution.hasLowercase("ABc"), true);
        check("hasLowercase is false without one", () -> Solution.hasLowercase("ABC1!"), false);
        check("hasUppercase finds an uppercase letter", () -> Solution.hasUppercase("abC"), true);
        check("hasUppercase is false without one", () -> Solution.hasUppercase("abc1!"), false);
        check("hasDigit finds a digit at the end", () -> Solution.hasDigit("abc1"), true);
        check("hasDigit finds 0 at the start", () -> Solution.hasDigit("0abc"), true);
        check("hasDigit finds 9 in the middle", () -> Solution.hasDigit("ab9c"), true);
        check("hasDigit is false without one", () -> Solution.hasDigit("abc"), false);
        check("hasSymbol counts punctuation", () -> Solution.hasSymbol("abc!"), true);
        check("hasSymbol counts a space", () -> Solution.hasSymbol("a b"), true);
        check("hasSymbol is false for letters and digits only", () -> Solution.hasSymbol("aB3"), false);
        check("hasLowercase returns false for an empty string", () -> Solution.hasLowercase(""), false);
        check("hasUppercase returns false for an empty string", () -> Solution.hasUppercase(""), false);
        check("hasDigit returns false for an empty string", () -> Solution.hasDigit(""), false);
        check("hasSymbol returns false for an empty string", () -> Solution.hasSymbol(""), false);
        check("empty password scores 0 and is weak", () -> Solution.passwordStrength(""), new Solution.Strength(0, "weak"));
        check("length 7 earns no length point", () -> Solution.passwordStrength("abcdefg"), new Solution.Strength(1, "weak"));
        check("length 8 earns a point, score 2 is still weak", () -> Solution.passwordStrength("abcdefgh"), new Solution.Strength(2, "weak"));
        check("score 3 is medium", () -> Solution.passwordStrength("abcdefgH"), new Solution.Strength(3, "medium"));
        check("score 4 is medium", () -> Solution.passwordStrength("ABCDEFGHIJK1"), new Solution.Strength(4, "medium"));
        check("score 5 is strong", () -> Solution.passwordStrength("Abcdefg1!"), new Solution.Strength(5, "strong"));
        check("length 11 does not earn the extra point", () -> Solution.passwordStrength("Abcdefghij1"), new Solution.Strength(4, "medium"));
        check("length 12 earns an extra point for a score of 6", () -> Solution.passwordStrength("Abcdefghij1!"), new Solution.Strength(6, "strong"));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
