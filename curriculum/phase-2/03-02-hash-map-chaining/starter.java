public class Solution {
    /** A string-keyed hash map with 8 starting buckets, chaining, and doubling past load factor 0.75. No java.util maps or sets. */
    public static class StringHashMap<V> {
        /** Stores value under key, replacing any existing value; grows if a new key pushed the load past 0.75. */
        public void set(String key, V value) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns the value stored under key, or null if there is none. */
        public V get(String key) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns whether key is stored, whatever its value. */
        public boolean has(String key) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Removes key and returns true, or returns false if it was not stored. */
        public boolean delete(String key) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns the number of stored keys. */
        public int size() {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** Returns the current number of buckets. */
        public int bucketCount() {
            throw new UnsupportedOperationException("Not implemented");
        }
    }
}
