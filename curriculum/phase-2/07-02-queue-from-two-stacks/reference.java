// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;

public class Solution {
    public static class TwoStackQueue<T> {
        private final ArrayList<T> incoming = new ArrayList<>();
        private final ArrayList<T> outgoing = new ArrayList<>();

        public void enqueue(T value) {
            incoming.add(value);
        }

        public T dequeue() {
            refill();
            return outgoing.isEmpty() ? null : outgoing.remove(outgoing.size() - 1);
        }

        public T peek() {
            refill();
            return outgoing.isEmpty() ? null : outgoing.get(outgoing.size() - 1);
        }

        public int size() {
            return incoming.size() + outgoing.size();
        }

        private void refill() {
            if (!outgoing.isEmpty()) return;
            while (!incoming.isEmpty()) outgoing.add(incoming.remove(incoming.size() - 1));
        }
    }
}
