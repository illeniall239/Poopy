import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
        check("counts repeated words in order of first appearance", () -> new ArrayList<>(Solution.wordFrequency("the cat and the hat").entrySet()),
            List.of(Map.entry("the", 2), Map.entry("cat", 1), Map.entry("and", 1), Map.entry("hat", 1)));
        check("case-insensitive with lowercase keys", () -> new ArrayList<>(Solution.wordFrequency("The THE the").entrySet()), List.of(Map.entry("the", 3)));
        check("punctuation separates words", () -> new ArrayList<>(Solution.wordFrequency("Hi, hi! HI?").entrySet()), List.of(Map.entry("hi", 3)));
        check("digits and apostrophes separate words", () -> new ArrayList<>(Solution.wordFrequency("abc123abc it's").entrySet()),
            List.of(Map.entry("abc", 2), Map.entry("it", 1), Map.entry("s", 1)));
        check("empty text has no words", () -> Solution.wordFrequency("").size(), 0);
        check("text without words has no entries", () -> Solution.wordFrequency("... 42 !").size(), 0);
        check("word at the very end is counted", () -> new ArrayList<>(Solution.wordFrequency("  go go").entrySet()), List.of(Map.entry("go", 2)));
        check("words that clash with common method names", () -> new ArrayList<>(Solution.wordFrequency("constructor toString constructor").entrySet()),
            List.of(Map.entry("constructor", 2), Map.entry("tostring", 1)));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
