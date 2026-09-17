import java.util.List;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable e) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + e);
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

    static String makeString(int n, int m, int mul) {
        StringBuilder s = new StringBuilder();
        for (int i = 0; i < n; i++) s.append("acgt".charAt(((i * i * mul + 3 * i + mul) % m) % 4));
        return s.toString();
    }

    public static void main(String[] args) {
        check("subsequence of the other string", () -> Solution.longestCommonSubsequence("abcde", "ace"), 3);
        check("identical strings", () -> Solution.longestCommonSubsequence("abc", "abc"), 3);
        check("no shared characters", () -> Solution.longestCommonSubsequence("abc", "def"), 0);
        check("empty string", () -> Solution.longestCommonSubsequence("", "abc"), 0);
        check("interleaved matches", () -> Solution.longestCommonSubsequence("AGGTAB", "GXTXAYB"), 4);
        check("repeated characters and case matters",
                () -> List.of(Solution.longestCommonSubsequence("aaaa", "aa"), Solution.longestCommonSubsequence("Abc", "abc")),
                List.of(2, 2));
        check("two 1000-character strings in O(n x m)",
                () -> Solution.longestCommonSubsequence(makeString(1000, 7, 1), makeString(1000, 11, 3)), 648);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
