import java.util.ArrayList;
import java.util.Arrays;
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

    /** "w" followed by the five digits of k (zero-padded) as the letters a..j, so numeric and alphabetical order agree. */
    static String wordFor(int k) {
        StringBuilder sb = new StringBuilder("w");
        for (char d : String.format("%05d", k).toCharArray()) sb.append((char) ('a' + (d - '0')));
        return sb.toString();
    }

    public static void main(String[] args) {
        check("first n matches in alphabetical order", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"apple", "app", "application", "apt", "banana"});
            return List.of(ac.suggest("app", 2), ac.suggest("app", 10), ac.suggest("ap", 1));
        }, List.of(List.of("app", "apple"), List.of("app", "apple", "application"), List.of("app")));

        check("a word equal to the prefix comes first", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"card", "cart", "car"});
            return ac.suggest("car", 3);
        }, List.of("car", "card", "cart"));

        check("no matches", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"apple", "banana"});
            return List.of(ac.suggest("c", 3), ac.suggest("apples", 3), ac.suggest("b", 3));
        }, List.of(List.of(), List.of(), List.of("banana")));

        check("n of zero", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"apple"});
            return List.of(ac.suggest("app", 0), ac.suggest("", 0));
        }, List.of(List.of(), List.of()));

        check("empty prefix gives the first n words overall", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"dog", "cat", "bird"});
            return List.of(ac.suggest("", 2), ac.suggest("", 5));
        }, List.of(List.of("bird", "cat"), List.of("bird", "cat", "dog")));

        check("duplicates are stored once", () -> {
            Solution.Autocomplete ac = new Solution.Autocomplete(new String[] {"a", "ab", "a", "ab", "a"});
            return ac.suggest("a", 5);
        }, List.of("a", "ab"));

        check("insertion order does not matter and the input is not changed", () -> {
            String[] words = {"band", "bandana", "banana", "ban"};
            Solution.Autocomplete ac = new Solution.Autocomplete(words);
            return List.of(ac.suggest("ban", 3), Arrays.toString(words));
        }, List.of(List.of("ban", "banana", "band"), "[band, bandana, banana, ban]"));

        check("100000 words and 100000 queries without scanning the list", () -> {
            int W = 100000;
            String[] words = new String[W];
            for (int i = 0; i < W; i++) words[i] = wordFor((int) ((i * 7919L) % W));
            Solution.Autocomplete ac = new Solution.Autocomplete(words);
            List<List<String>> got = new ArrayList<>();
            List<List<String>> expected = new ArrayList<>();
            for (int q = 0; q < W; q++) {
                int k = (int) ((q * 104729L) % W);
                int base = k - k % 100;
                got.add(ac.suggest(wordFor(k).substring(0, 4), 3));
                expected.add(List.of(wordFor(base), wordFor(base + 1), wordFor(base + 2)));
            }
            return got.equals(expected);
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
