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
        check("dots match any single letter", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            for (String w : new String[] {"bad", "dad", "mad"}) d.addWord(w);
            return List.of(d.search("pad"), d.search("bad"), d.search(".ad"), d.search("b.."));
        }, List.of(false, true, true, true));

        check("lengths must match", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            d.addWord("cat");
            return List.of(d.search("ca"), d.search("c."), d.search("c.t."), d.search("cats"));
        }, List.of(false, false, false, false));

        check("empty dictionary", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            return List.of(d.search("a"), d.search("."));
        }, List.of(false, false));

        check("a query of only dots matches any word of that length", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            d.addWord("hello");
            return List.of(d.search("....."), d.search("...."), d.search("......"));
        }, List.of(true, false, false));

        check("every branch under a dot is tried", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            for (String w : new String[] {"abc", "abd", "abx"}) d.addWord(w);
            return List.of(d.search("ab."), d.search("a.x"), d.search("a.y"), d.search("b.."));
        }, List.of(true, true, false, false));

        check("dots at the start and two dots", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            d.addWord("cab");
            d.addWord("dab");
            return List.of(d.search(".ab"), d.search("..b"), d.search("..c"), d.search(".a."));
        }, List.of(true, true, false, true));

        check("a prefix of a stored word is not a match", () -> {
            Solution.WordDictionary d = new Solution.WordDictionary();
            d.addWord("dog");
            d.addWord("dog");
            d.addWord("dogs");
            return List.of(d.search("do"), d.search("d."), d.search("dog"), d.search("d.g"), d.search("do.s"));
        }, List.of(false, false, true, true, true));

        check("50000 words and 150000 searches without scanning the words", () -> {
            int W = 50000;
            Solution.WordDictionary d = new Solution.WordDictionary();
            Set<String> words = new HashSet<>();
            Set<String> tailMasked = new HashSet<>();
            Set<String> headMasked = new HashSet<>();
            List<String> list = new ArrayList<>();
            for (int i = 0; i < W; i++) {
                String w = encode((i * 7919L) % 1000003);
                list.add(w);
                words.add(w);
                tailMasked.add(w.substring(0, 4));
                headMasked.add(w.substring(1));
                d.addWord(w);
            }
            List<Boolean> expected = new ArrayList<>();
            List<Boolean> got = new ArrayList<>();
            for (int q = 0; q < W; q++) {
                String s = q % 2 == 0 ? list.get(q) : encode((q * 104729L) % 1000003);
                expected.add(words.contains(s));
                expected.add(tailMasked.contains(s.substring(0, 4)));
                expected.add(headMasked.contains(s.substring(1)));
                got.add(d.search(s));
                got.add(d.search(s.substring(0, 4) + "."));
                got.add(d.search("." + s.substring(1)));
            }
            return got.equals(expected);
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
