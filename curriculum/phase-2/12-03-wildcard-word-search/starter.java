import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class WordDictionary {
        public WordDictionary() {
            throw new UnsupportedOperationException("Not implemented");
        }

        public void addWord(String word) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** True if some stored word matches query, where '.' matches any single letter. */
        public boolean search(String query) {
            throw new UnsupportedOperationException("Not implemented");
        }
    }
}
