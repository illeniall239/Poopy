// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static class DynamicArray<T> {
        private Object[] storage = new Object[1];
        private int count = 0;

        public int size() {
            return count;
        }

        public int capacity() {
            return storage.length;
        }

        public void push(T value) {
            if (count == storage.length) {
                Object[] bigger = new Object[storage.length * 2];
                for (int i = 0; i < count; i++) bigger[i] = storage[i];
                storage = bigger;
            }
            storage[count++] = value;
        }

        @SuppressWarnings("unchecked")
        public T get(int index) {
            checkIndex(index);
            return (T) storage[index];
        }

        public void set(int index, T value) {
            checkIndex(index);
            storage[index] = value;
        }

        @SuppressWarnings("unchecked")
        public T pop() {
            if (count == 0) throw new IndexOutOfBoundsException("pop from empty DynamicArray");
            T value = (T) storage[--count];
            storage[count] = null;
            return value;
        }

        @SuppressWarnings("unchecked")
        public List<T> toList() {
            List<T> result = new ArrayList<>(count);
            for (int i = 0; i < count; i++) result.add((T) storage[i]);
            return result;
        }

        private void checkIndex(int index) {
            if (index < 0 || index >= count) throw new IndexOutOfBoundsException("index " + index + " out of range");
        }
    }
}
