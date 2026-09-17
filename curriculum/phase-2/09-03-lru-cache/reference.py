# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev: "_Node" = self
        self.next: "_Node" = self


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._nodes: dict[int, _Node] = {}
        # One sentinel: sentinel.next is the most recently used, sentinel.prev the least.
        self._sentinel = _Node(-1, -1)

    def get(self, key: int) -> int:
        node = self._nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self._nodes.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._nodes) == self._capacity:
            oldest = self._sentinel.prev
            self._unlink(oldest)
            del self._nodes[oldest.key]
        node = _Node(key, value)
        self._nodes[key] = node
        self._push_front(node)

    def _unlink(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev = self._sentinel
        node.next = self._sentinel.next
        self._sentinel.next.prev = node
        self._sentinel.next = node
