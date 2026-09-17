# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import asyncio
from typing import Awaitable, Callable

FetchPage = Callable[[str], Awaitable[str]]


async def fetch_all(urls: list[str], fetch_page: FetchPage) -> list[str]:
    return list(await asyncio.gather(*(fetch_page(url) for url in urls)))


async def fetch_one_by_one(urls: list[str], fetch_page: FetchPage) -> list[str]:
    pages: list[str] = []
    for url in urls:
        pages.append(await fetch_page(url))
    return pages
