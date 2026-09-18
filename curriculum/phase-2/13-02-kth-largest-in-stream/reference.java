// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.PriorityQueue;

public class Solution {
    public static class KthLargest {
        private final int k;
        private final PriorityQueue<Integer> heap = new PriorityQueue<>();

        public KthLargest(int k) {
            this.k = k;
        }

        public Integer add(int value) {
            if (heap.size() < k) {
                heap.add(value);
            } else if (value > heap.peek()) {
                heap.poll();
                heap.add(value);
            }
            return heap.size() == k ? heap.peek() : null;
        }
    }
}
