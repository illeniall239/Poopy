# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end_of_word = True

    def search(self, query: str) -> bool:
        def matches(node: TrieNode, i: int) -> bool:
            if i == len(query):
                return node.is_end_of_word
            ch = query[i]
            if ch != ".":
                nxt = node.children.get(ch)
                return nxt is not None and matches(nxt, i + 1)
            return any(matches(child, i + 1) for child in node.children.values())

        return matches(self.root, 0)
