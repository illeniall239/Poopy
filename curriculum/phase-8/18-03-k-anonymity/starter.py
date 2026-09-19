def k_anonymity(records: list[dict], quasi_ids: list[str]) -> int:
    """Size of the smallest group of records sharing the same quasi-identifier values."""
    raise NotImplementedError


def generalize(records: list[dict], quasi_ids: list[str], rules: dict, k: int) -> list[dict]:
    """Raise quasi-identifier generalization levels (lowest level first) until the records are k-anonymous."""
    raise NotImplementedError
