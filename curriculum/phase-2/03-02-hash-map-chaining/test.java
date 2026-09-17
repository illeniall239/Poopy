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
        check("set and get, missing keys give null", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            m.set("apple", 1);
            m.set("pear", 2);
            return Arrays.asList(m.get("apple"), m.get("pear"), m.get("plum"), m.size(), m.bucketCount());
        }, Arrays.asList(1, 2, null, 2, 8));
        check("setting an existing key replaces the value, not the size", () -> {
            Solution.StringHashMap<String> m = new Solution.StringHashMap<>();
            m.set("k", "old");
            m.set("k", "new");
            return List.of(m.get("k"), m.size());
        }, List.of("new", 1));
        check("keys with the same characters and the empty key are all distinct", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            m.set("ab", 1);
            m.set("ba", 2);
            m.set("listen", 3);
            m.set("silent", 4);
            m.set("", 5);
            return List.of(m.get("ab"), m.get("ba"), m.get("listen"), m.get("silent"), m.get(""), m.size());
        }, List.of(1, 2, 3, 4, 5, 5));
        check("has is true for stored falsy values", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            m.set("zero", 0);
            m.set("nothing", null);
            return Arrays.asList(m.has("zero"), m.has("nothing"), m.has("other"), m.get("zero"));
        }, Arrays.asList(true, true, false, 0));
        check("delete removes only that key and reports whether it was there", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            m.set("ab", 1);
            m.set("ba", 2);
            List<Object> results = new ArrayList<>();
            results.add(m.delete("ab"));
            results.add(m.delete("ab"));
            results.add(m.delete("never"));
            results.add(m.get("ab"));
            results.add(m.has("ab"));
            results.add(m.get("ba"));
            results.add(m.size());
            m.set("ab", 7);
            results.add(m.size());
            return results;
        }, Arrays.asList(true, false, false, null, false, 2, 1, 2));
        check("doubles the buckets only when the load factor passes 0.75", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            List<Integer> counts = new ArrayList<>();
            for (int i = 1; i <= 13; i++) {
                m.set("k" + i, i);
                m.set("k" + i, i + 100);
                counts.add(m.bucketCount());
            }
            return counts;
        }, List.of(8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 32));
        check("every entry survives resizing", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            for (int i = 0; i < 100; i++) m.set("item-" + i, i * i);
            List<String> wrong = new ArrayList<>();
            for (int i = 0; i < 100; i++) if (!Objects.equals(m.get("item-" + i), i * i)) wrong.add("item-" + i);
            return List.of(wrong, m.size(), m.bucketCount());
        }, List.of(List.of(), 100, 256));
        check("400000 keys with O(1) average operations", () -> {
            Solution.StringHashMap<Integer> m = new Solution.StringHashMap<>();
            int n = 400000;
            for (int i = 0; i < n; i++) m.set("key" + i, i);
            int wrong = 0;
            for (int i = 0; i < n; i++) if (!Objects.equals(m.get("key" + i), i)) wrong++;
            return List.of(wrong, m.size(), m.bucketCount());
        }, List.of(0, 400000, 1048576));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
