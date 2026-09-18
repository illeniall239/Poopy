// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.HashMap;

public class Solution {
    public static class LRUCache {
        private static class Node {
            int key, value;
            Node prev, next;

            Node(int key, int value) {
                this.key = key;
                this.value = value;
            }
        }

        private final int capacity;
        private final HashMap<Integer, Node> nodes = new HashMap<>();
        // Sentinels: head.next is the most recently used, tail.prev the least.
        private final Node head = new Node(-1, -1), tail = new Node(-1, -1);

        public LRUCache(int capacity) {
            this.capacity = capacity;
            head.next = tail;
            tail.prev = head;
        }

        public int get(int key) {
            Node node = nodes.get(key);
            if (node == null) return -1;
            unlink(node);
            pushFront(node);
            return node.value;
        }

        public void put(int key, int value) {
            Node node = nodes.get(key);
            if (node != null) {
                node.value = value;
                unlink(node);
                pushFront(node);
                return;
            }
            if (nodes.size() == capacity) {
                Node oldest = tail.prev;
                unlink(oldest);
                nodes.remove(oldest.key);
            }
            node = new Node(key, value);
            nodes.put(key, node);
            pushFront(node);
        }

        private void unlink(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        private void pushFront(Node node) {
            node.prev = head;
            node.next = head.next;
            head.next.prev = node;
            head.next = node;
        }
    }
}
