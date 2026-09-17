from typing import Awaitable, Callable

FetchPage = Callable[[str], Awaitable[str]]


async def fetch_all(urls: list[str], fetch_page: FetchPage) -> list[str]:
    """Fetch every url at the same time and return the pages in input order."""
    raise NotImplementedError


async def fetch_one_by_one(urls: list[str], fetch_page: FetchPage) -> list[str]:
    """Fetch the urls strictly one after another and return the pages in input order."""
    raise NotImplementedError
