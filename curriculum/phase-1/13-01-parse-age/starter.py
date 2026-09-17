class RangeError(ValueError):
    """Raised when the age is a whole number but outside 0 to 150."""


def parse_age(input: str) -> int:
    """Parse a whole-number age from 0 to 150; raise ValueError (or RangeError if out of range) with a descriptive message."""
    raise NotImplementedError
