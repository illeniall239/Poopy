import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;
import java.util.ArrayList;
import java.util.List;

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
        check("groups anagrams in order of first appearance", () -> Solution.groupAnagrams(List.of("eat", "tea", "tan", "ate", "nat", "bat")),
            List.of(List.of("eat", "tea", "ate"), List.of("tan", "nat"), List.of("bat")));
        check("different lengths are never anagrams", () -> Solution.groupAnagrams(List.of("ab", "abc", "ba")), List.of(List.of("ab", "ba"), List.of("abc")));
        check("empty input", () -> Solution.groupAnagrams(List.of()), List.of());
        check("no anagrams gives one group per word", () -> Solution.groupAnagrams(List.of("cat", "dog", "bird")), List.of(List.of("cat"), List.of("dog"), List.of("bird")));
        check("same letters but different counts are not anagrams", () -> Solution.groupAnagrams(List.of("aab", "abb", "bab")), List.of(List.of("aab"), List.of("abb", "bab")));
        check("duplicate words stay in the same group", () -> Solution.groupAnagrams(List.of("stop", "pots", "stop")), List.of(List.of("stop", "pots", "stop")));
        check("does not modify the input", () -> {
            List<String> words = new ArrayList<>(List.of("tops", "spot", "a"));
            Solution.groupAnagrams(words);
            return words;
        }, List.of("tops", "spot", "a"));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
