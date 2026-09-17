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
        check("values come out in the order they went in", () -> {
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            q.enqueue(1);
            q.enqueue(2);
            q.enqueue(3);
            return List.of(q.dequeue(), q.dequeue(), q.dequeue());
        }, List.of(1, 2, 3));
        check("peek returns the front without removing it", () -> {
            Solution.TwoStackQueue<String> q = new Solution.TwoStackQueue<>();
            q.enqueue("a");
            q.enqueue("b");
            return List.of(q.peek(), q.peek(), q.size(), q.dequeue());
        }, List.of("a", "a", 2, "a"));
        check("mixed enqueues and dequeues keep FIFO order", () -> {
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            q.enqueue(1);
            q.enqueue(2);
            Integer first = q.dequeue();
            q.enqueue(3);
            q.enqueue(4);
            Integer second = q.dequeue();
            q.enqueue(5);
            return List.of(first, second, q.dequeue(), q.dequeue(), q.dequeue());
        }, List.of(1, 2, 3, 4, 5));
        check("empty queue returns null and size 0", () -> {
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            return Arrays.asList(q.size(), q.dequeue(), q.peek(), q.size());
        }, Arrays.asList(0, null, null, 0));
        check("size counts values on both sides", () -> {
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            q.enqueue(1);
            q.enqueue(2);
            q.dequeue();
            q.enqueue(3);
            q.enqueue(4);
            return q.size();
        }, 3);
        check("dequeue on an empty queue changes nothing", () -> {
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            q.dequeue();
            q.enqueue(7);
            return List.of(q.size(), q.dequeue(), q.size());
        }, List.of(1, 7, 0));
        check("separate queues don't share values", () -> {
            Solution.TwoStackQueue<Integer> a = new Solution.TwoStackQueue<>();
            Solution.TwoStackQueue<Integer> b = new Solution.TwoStackQueue<>();
            a.enqueue(1);
            b.enqueue(2);
            return List.of(a.dequeue(), b.dequeue(), a.size(), b.size());
        }, List.of(1, 2, 0, 0));
        check("200000 values with 200000 mixed calls, amortized O(1)", () -> {
            int n = 200000;
            Solution.TwoStackQueue<Integer> q = new Solution.TwoStackQueue<>();
            for (int i = 0; i < n; i++) q.enqueue(i);
            int wrong = 0;
            for (int i = 0; i < n; i++) {
                if (!Objects.equals(q.peek(), i)) wrong++;
                if (!Objects.equals(q.dequeue(), i)) wrong++;
                q.enqueue(n + i);
            }
            return List.of(wrong, q.size(), q.peek());
        }, List.of(0, 200000, 200000));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
