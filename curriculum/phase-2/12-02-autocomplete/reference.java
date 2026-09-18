// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class Autocomplete {
        private final TrieNode root = new TrieNode();

        public Autocomplete(String[] words) {
            for (String word : words) {
                TrieNode node = root;
                for (char ch : word.toCharArray()) node = node.children.computeIfAbsent(ch, k -> new TrieNode());
                node.isEndOfWord = true;
            }
        }

        public List<String> suggest(String prefix, int n) {
            TrieNode node = root;
            for (char ch : prefix.toCharArray()) {
                node = node.children.get(ch);
                if (node == null) return new ArrayList<>();
            }
            List<String> out = new ArrayList<>();
            collect(node, new StringBuilder(prefix), n, out);
            return out;
        }

        private static void collect(TrieNode node, StringBuilder path, int n, List<String> out) {
            if (out.size() >= n) return;
            if (node.isEndOfWord) out.add(path.toString());
            for (Map.Entry<Character, TrieNode> e : new TreeMap<>(node.children).entrySet()) {
                if (out.size() >= n) return;
                path.append(e.getKey());
                collect(e.getValue(), path, n, out);
                path.setLength(path.length() - 1);
            }
        }
    }
}
