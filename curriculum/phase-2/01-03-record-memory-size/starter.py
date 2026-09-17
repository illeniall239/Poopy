def record_size(fields: list[str]) -> int:
    """Return the size in bytes of a record with these fields, including alignment padding."""
    raise NotImplementedError


def array_size(fields: list[str], count: int) -> int:
    """Return the bytes used by count such records stored back to back."""
    raise NotImplementedError
