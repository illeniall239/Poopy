import java.util.HashSet;
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

    public static void main(String[] args) {
        check("two characters", () -> Solution.permutations("ab"), List.of("ab", "ba"));
        check("three characters, sorted", () -> Solution.permutations("abc"), List.of("abc", "acb", "bac", "bca", "cab", "cba"));
        check("input order does not change the sorted result", () -> Solution.permutations("cba"), List.of("abc", "acb", "bac", "bca", "cab", "cba"));
        check("repeated characters give distinct results only",
            () -> List.of(Solution.permutations("aab"), Solution.permutations("aaa")),
            List.of(List.of("aab", "aba", "baa"), List.of("aaa")));
        check("single character", () -> Solution.permutations("a"), List.of("a"));
        check("empty string has one ordering", () -> Solution.permutations(""), List.of(""));
        check("eight distinct characters give 40320 distinct results", () -> {
            List<String> result = Solution.permutations("abcdefgh");
            return List.of(result.size(), new HashSet<>(result).size(), result.get(0), result.get(40319));
        }, List.of(40320, 40320, "abcdefgh", "hgfedcba"));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
