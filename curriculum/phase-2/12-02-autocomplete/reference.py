# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class Autocomplete:
    def __init__(self, words: list[str]) -> None:
        self.root = TrieNode()
        for word in words:
            node = self.root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end_of_word = True

    def suggest(self, prefix: str, n: int) -> list[str]:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return []
        out: list[str] = []

        def collect(cur: TrieNode, path: str) -> None:
            if len(out) >= n:
                return
            if cur.is_end_of_word:
                out.append(path)
            for ch in sorted(cur.children):
                if len(out) >= n:
                    return
                collect(cur.children[ch], path + ch)

        collect(node, prefix)
        return out
