class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class WordDictionary:
    def __init__(self) -> None:
        raise NotImplementedError

    def add_word(self, word: str) -> None:
        raise NotImplementedError

    def search(self, query: str) -> bool:
        """True if some stored word matches query, where "." matches any single letter."""
        raise NotImplementedError
