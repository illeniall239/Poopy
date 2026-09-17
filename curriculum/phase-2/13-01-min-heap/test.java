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

    static List<Integer> drain(Solution.MinHeap heap) {
        List<Integer> out = new ArrayList<>();
        while (heap.size() > 0) out.add(heap.pop());
        return out;
    }

    public static void main(String[] args) {
        check("empty heap has size 0 and returns null", () -> {
            Solution.MinHeap heap = new Solution.MinHeap();
            return Arrays.asList(heap.size(), heap.peek(), heap.pop());
        }, Arrays.asList(0, null, null));

        check("peek returns the smallest without removing it", () -> {
            Solution.MinHeap heap = new Solution.MinHeap();
            heap.push(5);
            heap.push(3);
            heap.push(8);
            return List.of(heap.peek(), heap.size());
        }, List.of(3, 3));

        check("pops come out smallest first, duplicates included", () -> {
            Solution.MinHeap heap = new Solution.MinHeap();
            for (int v : new int[] {5, 3, 8, 3, 1, 9, 2}) heap.push(v);
            List<Integer> out = drain(heap);
            out.add(heap.pop());
            return out;
        }, Arrays.asList(1, 2, 3, 3, 5, 8, 9, null));

        check("negative numbers", () -> {
            Solution.MinHeap heap = new Solution.MinHeap();
            for (int v : new int[] {0, -4, 7, -10, 2}) heap.push(v);
            return drain(heap);
        }, List.of(-10, -4, 0, 2, 7));

        check("interleaved push and pop", () -> {
            Solution.MinHeap heap = new Solution.MinHeap();
            heap.push(4);
            heap.push(7);
            Integer a = heap.pop();
            heap.push(1);
            heap.push(6);
            Integer b = heap.pop();
            return List.of(a, b, heap.peek(), heap.size());
        }, List.of(4, 1, 6, 2));

        check("builds from a starting array without changing it", () -> {
            int[] values = {9, 4, 7, 1, 8, 2};
            Solution.MinHeap heap = new Solution.MinHeap(values);
            return List.of(heap.size(), drain(heap), Arrays.toString(values));
        }, List.of(6, List.of(1, 2, 4, 7, 8, 9), "[9, 4, 7, 1, 8, 2]"));

        check("200 000 pushes then pops, O(log n) each", () -> {
            int n = 200000;
            Solution.MinHeap heap = new Solution.MinHeap();
            int[] values = new int[n];
            for (int i = 0; i < n; i++) {
                values[i] = (int) ((i * 7919L) % 200003);
                heap.push(values[i]);
            }
            Arrays.sort(values);
            List<Integer> expected = new ArrayList<>();
            for (int v : values) expected.add(v);
            return drain(heap).equals(expected);
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
