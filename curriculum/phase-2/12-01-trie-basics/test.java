import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
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

    /** Five lowercase letters encoding x (0 <= x < 26^5), most significant first. */
    static String encode(long x) {
        char[] s = new char[5];
        for (int k = 4; k >= 0; k--) {
            s[k] = (char) ('a' + x % 26);
            x /= 26;
        }
        return new String(s);
    }

    public static void main(String[] args) {
        check("whole word versus its beginning", () -> {
            Solution.Trie trie = new Solution.Trie();
            trie.insert("apple");
            return List.of(trie.search("apple"), trie.search("app"), trie.startsWith("app"));
        }, List.of(true, false, true));

        check("a prefix becomes a word once inserted", () -> {
            Solution.Trie trie = new Solution.Trie();
            trie.insert("apple");
            trie.insert("app");
            return List.of(trie.search("app"), trie.search("apple"));
        }, List.of(true, true));

        check("empty trie answers false", () -> {
            Solution.Trie trie = new Solution.Trie();
            return List.of(trie.search("a"), trie.startsWith("a"));
        }, List.of(false, false));

        check("words sharing a beginning", () -> {
            Solution.Trie trie = new Solution.Trie();
            for (String w : new String[] {"car", "cart", "cat"}) trie.insert(w);
            return List.of(trie.search("car"), trie.search("cart"), trie.search("cat"), trie.search("ca"),
                    trie.startsWith("ca"), trie.startsWith("cab"), trie.startsWith("cart"));
        }, List.of(true, true, true, false, true, false, true));

        check("inserting the same word twice changes nothing", () -> {
            Solution.Trie trie = new Solution.Trie();
            trie.insert("dog");
            trie.insert("dog");
            return List.of(trie.search("dog"), trie.search("do"), trie.startsWith("dog"));
        }, List.of(true, false, true));

        check("query longer than any stored word", () -> {
            Solution.Trie trie = new Solution.Trie();
            trie.insert("cat");
            return List.of(trie.search("cats"), trie.startsWith("cats"));
        }, List.of(false, false));

        check("different first letters", () -> {
            Solution.Trie trie = new Solution.Trie();
            for (String w : new String[] {"dog", "dot", "cat"}) trie.insert(w);
            return List.of(trie.startsWith("d"), trie.startsWith("c"), trie.startsWith("e"), trie.search("d"));
        }, List.of(true, true, false, false));

        check("50000 words and 100000 queries in O(L) each", () -> {
            int W = 50000;
            Solution.Trie trie = new Solution.Trie();
            Set<String> words = new HashSet<>();
            Set<String> prefixes = new HashSet<>();
            List<String> list = new ArrayList<>();
            for (int i = 0; i < W; i++) {
                String w = encode((i * 7919L) % 1000003);
                list.add(w);
                words.add(w);
                prefixes.add(w.substring(0, 4));
                trie.insert(w);
            }
            List<Boolean> expected = new ArrayList<>();
            List<Boolean> got = new ArrayList<>();
            for (int q = 0; q < W; q++) {
                String s = q % 2 == 0 ? list.get(q) : encode((q * 104729L) % 1000003);
                expected.add(words.contains(s));
                expected.add(prefixes.contains(s.substring(0, 4)));
                got.add(trie.search(s));
                got.add(trie.startsWith(s.substring(0, 4)));
            }
            return got.equals(expected);
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
