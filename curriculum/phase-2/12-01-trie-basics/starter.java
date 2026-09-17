import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class Trie {
        public Trie() {
            throw new UnsupportedOperationException("Not implemented");
        }

        public void insert(String word) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** True if exactly this word was inserted. */
        public boolean search(String word) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** True if at least one inserted word begins with prefix. */
        public boolean startsWith(String prefix) {
            throw new UnsupportedOperationException("Not implemented");
        }
    }
}
