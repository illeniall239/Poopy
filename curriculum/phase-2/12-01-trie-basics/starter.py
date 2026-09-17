class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        """True if exactly this word was inserted."""
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        """True if at least one inserted word begins with prefix."""
        raise NotImplementedError
