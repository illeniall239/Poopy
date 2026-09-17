class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class Autocomplete:
    def __init__(self, words: list[str]) -> None:
        """Stores every word once. Must not change the list passed in."""
        raise NotImplementedError

    def suggest(self, prefix: str, n: int) -> list[str]:
        """The first n stored words in alphabetical order that begin with prefix."""
        raise NotImplementedError
