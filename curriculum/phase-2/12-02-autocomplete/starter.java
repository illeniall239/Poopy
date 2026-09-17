import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static class TrieNode {
        public Map<Character, TrieNode> children = new HashMap<>();
        public boolean isEndOfWord = false;
    }

    public static class Autocomplete {
        /** Stores every word once. Must not change the array passed in. */
        public Autocomplete(String[] words) {
            throw new UnsupportedOperationException("Not implemented");
        }

        /** The first n stored words in alphabetical order that begin with prefix. */
        public List<String> suggest(String prefix, int n) {
            throw new UnsupportedOperationException("Not implemented");
        }
    }
}
