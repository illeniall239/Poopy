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
        check("evicts the least recently used entry when full", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(2);
            cache.put(1, 100);
            cache.put(2, 200);
            int got1 = cache.get(1);
            cache.put(3, 300);
            return List.of(got1, cache.get(2), cache.get(1), cache.get(3));
        }, List.of(100, -1, 100, 300));
        check("missing key returns -1", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(3);
            int first = cache.get(42);
            cache.put(1, 5);
            return List.of(first, cache.get(2));
        }, List.of(-1, -1));
        check("put on an existing key updates the value without evicting", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(2);
            cache.put(1, 100);
            cache.put(2, 200);
            cache.put(1, 111);
            return List.of(cache.get(1), cache.get(2));
        }, List.of(111, 200));
        check("put on an existing key counts as a use", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(2);
            cache.put(1, 100);
            cache.put(2, 200);
            cache.put(1, 111);
            cache.put(3, 300);
            return List.of(cache.get(2), cache.get(1), cache.get(3));
        }, List.of(-1, 111, 300));
        check("get counts as a use, but a missing get does not", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(2);
            cache.put(1, 100);
            cache.put(2, 200);
            cache.get(1);
            cache.get(9);
            cache.put(3, 300);
            return List.of(cache.get(2), cache.get(1), cache.get(3));
        }, List.of(-1, 100, 300));
        check("capacity 1 keeps only the latest entry", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(1);
            cache.put(1, 100);
            cache.put(2, 200);
            return List.of(cache.get(1), cache.get(2));
        }, List.of(-1, 200));
        check("0 is a stored value, not a missing one", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(2);
            cache.put(0, 0);
            cache.put(7, 0);
            return List.of(cache.get(0), cache.get(7));
        }, List.of(0, 0));
        check("longer sequence of mixed calls", () -> {
            Solution.LRUCache cache = new Solution.LRUCache(3);
            cache.put(1, 1);
            cache.put(2, 2);
            cache.put(3, 3);
            cache.get(1);
            cache.put(4, 4);
            cache.get(3);
            cache.put(5, 5);
            cache.put(1, 10);
            cache.put(6, 6);
            return List.of(cache.get(1), cache.get(2), cache.get(3), cache.get(4), cache.get(5), cache.get(6));
        }, List.of(10, -1, -1, -1, 5, 6));
        check("100000 entries and 600000 calls in O(1) each", () -> {
            int cap = 100000, calls = 500000;
            Solution.LRUCache cache = new Solution.LRUCache(cap);
            for (int k = 0; k < cap; k++) cache.put(k, 2 * k);
            int wrong = 0;
            for (int i = 0; i < calls; i++) {
                int k = (int) ((i * 7919L) % cap);
                if (cache.get(k) != 2 * k) wrong++;
            }
            // The last get touched this key, so it is the most recently used.
            int newest = (int) (((calls - 1) * 7919L) % cap);
            for (int k = cap; k < 2 * cap - 1; k++) cache.put(k, 2 * k);
            if (cache.get(newest) != 2 * newest) wrong++;
            for (int k = 0; k < cap; k += 997) if (k != newest && cache.get(k) != -1) wrong++;
            for (int k = cap; k < 2 * cap - 1; k += 991) if (cache.get(k) != 2 * k) wrong++;
            return wrong;
        }, 0);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
