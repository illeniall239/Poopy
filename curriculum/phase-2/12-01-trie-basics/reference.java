// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class Trie {
        private final TrieNode root = new TrieNode();

        public Trie() {
        }

        public void insert(String word) {
            TrieNode node = root;
            for (char ch : word.toCharArray()) node = node.children.computeIfAbsent(ch, k -> new TrieNode());
            node.isEndOfWord = true;
        }

        private TrieNode walk(String s) {
            TrieNode node = root;
            for (char ch : s.toCharArray()) {
                node = node.children.get(ch);
                if (node == null) return null;
            }
            return node;
        }

        public boolean search(String word) {
            TrieNode node = walk(word);
            return node != null && node.isEndOfWord;
        }

        public boolean startsWith(String prefix) {
            return walk(prefix) != null;
        }
    }
}
