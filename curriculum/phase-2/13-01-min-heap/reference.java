// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.Arrays;

public class Solution {
    public static class MinHeap {
        private int[] items;
        private int count;

        public MinHeap() {
            items = new int[16];
        }

        public MinHeap(int[] values) {
            items = Arrays.copyOf(values, Math.max(16, values.length));
            count = values.length;
            for (int i = count / 2 - 1; i >= 0; i--) siftDown(i);
        }

        public void push(int value) {
            if (count == items.length) items = Arrays.copyOf(items, items.length * 2);
            items[count] = value;
            int i = count++;
            while (i > 0) {
                int parent = (i - 1) / 2;
                if (items[parent] <= items[i]) break;
                swap(parent, i);
                i = parent;
            }
        }

        public Integer pop() {
            if (count == 0) return null;
            int top = items[0];
            items[0] = items[--count];
            siftDown(0);
            return top;
        }

        public Integer peek() {
            return count == 0 ? null : items[0];
        }

        public int size() {
            return count;
        }

        private void siftDown(int i) {
            while (true) {
                int l = 2 * i + 1, r = 2 * i + 2, smallest = i;
                if (l < count && items[l] < items[smallest]) smallest = l;
                if (r < count && items[r] < items[smallest]) smallest = r;
                if (smallest == i) return;
                swap(smallest, i);
                i = smallest;
            }
        }

        private void swap(int a, int b) {
            int t = items[a];
            items[a] = items[b];
            items[b] = t;
        }
    }
}
