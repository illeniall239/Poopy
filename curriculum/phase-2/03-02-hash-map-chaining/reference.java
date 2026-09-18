// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static class StringHashMap<V> {
        private static final class Entry<V> {
            final String key;
            V value;
            Entry<V> next;

            Entry(String key, V value, Entry<V> next) {
                this.key = key;
                this.value = value;
                this.next = next;
            }
        }

        @SuppressWarnings("unchecked")
        private Entry<V>[] buckets = (Entry<V>[]) new Entry[8];
        private int count = 0;

        private static int indexFor(String key, int bucketCount) {
            int hash = 0;
            for (int i = 0; i < key.length(); i++) hash = hash * 31 + key.charAt(i);
            return Math.floorMod(hash, bucketCount);
        }

        private Entry<V> find(String key) {
            for (Entry<V> e = buckets[indexFor(key, buckets.length)]; e != null; e = e.next) {
                if (e.key.equals(key)) return e;
            }
            return null;
        }

        public void set(String key, V value) {
            Entry<V> existing = find(key);
            if (existing != null) {
                existing.value = value;
                return;
            }
            int index = indexFor(key, buckets.length);
            buckets[index] = new Entry<>(key, value, buckets[index]);
            count++;
            if ((double) count / buckets.length > 0.75) resize();
        }

        public V get(String key) {
            Entry<V> e = find(key);
            return e == null ? null : e.value;
        }

        public boolean has(String key) {
            return find(key) != null;
        }

        public boolean delete(String key) {
            int index = indexFor(key, buckets.length);
            Entry<V> prev = null;
            for (Entry<V> e = buckets[index]; e != null; prev = e, e = e.next) {
                if (e.key.equals(key)) {
                    if (prev == null) buckets[index] = e.next;
                    else prev.next = e.next;
                    count--;
                    return true;
                }
            }
            return false;
        }

        public int size() {
            return count;
        }

        public int bucketCount() {
            return buckets.length;
        }

        @SuppressWarnings("unchecked")
        private void resize() {
            Entry<V>[] bigger = (Entry<V>[]) new Entry[buckets.length * 2];
            for (Entry<V> head : buckets) {
                Entry<V> e = head;
                while (e != null) {
                    Entry<V> next = e.next;
                    int index = indexFor(e.key, bigger.length);
                    e.next = bigger[index];
                    bigger[index] = e;
                    e = next;
                }
            }
            buckets = bigger;
        }
    }
}
