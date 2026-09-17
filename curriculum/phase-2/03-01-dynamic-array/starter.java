import java.util.List;

public class Solution {
    /** A growable array on fixed-capacity Object[] storage that doubles when full. */
    public static class DynamicArray<T> {
        /** Returns how many elements are stored. */
        public int size() {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns how many elements fit in the current storage. */
        public int capacity() {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Adds value at the end, doubling the storage first if it is full. */
        public void push(T value) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns the element at index; throws IndexOutOfBoundsException unless 0 <= index < size(). */
        public T get(int index) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Replaces the element at index; throws IndexOutOfBoundsException unless 0 <= index < size(). */
        public void set(int index, T value) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Removes and returns the last element; throws IndexOutOfBoundsException when empty. */
        public T pop() {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns a new list of the elements in order. */
        public List<T> toList() {
            throw new UnsupportedOperationException("Not implemented");
        }
    }
}
