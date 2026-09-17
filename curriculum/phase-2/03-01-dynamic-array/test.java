import java.util.ArrayList;
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

    /** Returns "threw" if action throws IndexOutOfBoundsException, "no error" if it completes; other exceptions propagate. */
    static String outOfBounds(Runnable action) {
        try {
            action.run();
            return "no error";
        } catch (IndexOutOfBoundsException e) {
            return "threw";
        }
    }

    public static void main(String[] args) {
        check("starts empty with capacity 1", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            return List.of(a.size(), a.capacity(), a.toList());
        }, List.of(0, 1, List.of()));
        check("push then get keeps order", () -> {
            Solution.DynamicArray<String> a = new Solution.DynamicArray<>();
            a.push("x");
            a.push("y");
            a.push("z");
            return List.of(a.size(), a.get(0), a.get(1), a.get(2));
        }, List.of(3, "x", "y", "z"));
        check("capacity doubles only when full", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            List<Integer> capacities = new ArrayList<>();
            for (int i = 0; i < 5; i++) {
                a.push(i);
                capacities.add(a.capacity());
            }
            return capacities;
        }, List.of(1, 2, 4, 4, 8));
        check("get and set throw outside 0..size-1, even below capacity", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            a.push(1);
            a.push(2);
            a.push(3);
            return List.of(a.capacity(), outOfBounds(() -> a.get(3)), outOfBounds(() -> a.get(-1)), outOfBounds(() -> a.set(3, 9)));
        }, List.of(4, "threw", "threw", "threw"));
        check("set replaces a value without changing the size", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            a.push(1);
            a.push(2);
            a.set(0, 7);
            return List.of(a.toList(), a.size());
        }, List.of(List.of(7, 2), 2));
        check("pop returns the last element and never shrinks capacity", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            a.push(1);
            a.push(2);
            a.push(3);
            int first = a.pop();
            int second = a.pop();
            int size = a.size();
            int capacity = a.capacity();
            String getGone = outOfBounds(() -> a.get(1));
            int last = a.pop();
            return List.of(first, second, size, capacity, getGone, last, outOfBounds(a::pop));
        }, List.of(3, 2, 1, 4, "threw", 1, "threw"));
        check("toList returns a copy that can't break the structure", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            a.push(1);
            a.push(2);
            a.push(3);
            List<Integer> copy = a.toList();
            int length = copy.size();
            copy.set(0, 99);
            copy.add(100);
            return List.of(length, a.toList(), a.size());
        }, List.of(3, List.of(1, 2, 3), 3));
        check("1000000 pushes with amortized O(1) push", () -> {
            Solution.DynamicArray<Integer> a = new Solution.DynamicArray<>();
            int n = 1000000;
            for (int i = 0; i < n; i++) a.push(i);
            return List.of(a.size(), a.capacity(), a.get(n - 1), a.get(123456));
        }, List.of(1000000, 1048576, 999999, 123456));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
