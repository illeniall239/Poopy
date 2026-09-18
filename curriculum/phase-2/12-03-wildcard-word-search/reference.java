// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class WordDictionary {
        private final TrieNode root = new TrieNode();

        public WordDictionary() {
        }

        public void addWord(String word) {
            TrieNode node = root;
            for (char ch : word.toCharArray()) node = node.children.computeIfAbsent(ch, k -> new TrieNode());
            node.isEndOfWord = true;
        }

        public boolean search(String query) {
            return matches(root, query, 0);
        }

        private static boolean matches(TrieNode node, String query, int i) {
            if (i == query.length()) return node.isEndOfWord;
            char ch = query.charAt(i);
            if (ch != '.') {
                TrieNode next = node.children.get(ch);
                return next != null && matches(next, query, i + 1);
            }
            for (TrieNode child : node.children.values()) {
                if (matches(child, query, i + 1)) return true;
            }
            return false;
        }
    }
}
