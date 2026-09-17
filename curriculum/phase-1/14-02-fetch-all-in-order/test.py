import asyncio
import unittest

from solution import fetch_all, fetch_one_by_one

delays = {"a": 30, "b": 10, "c": 20, "bad": 5, "slow": 40}


def fake_fetcher():
    """Return (fetch_page, log): fetch_page records when each download starts and ends. "bad" fails."""
    log = []

    async def fetch_page(url):
        log.append(f"start {url}")
        await asyncio.sleep(delays[url] / 1000)
        log.append(f"end {url}")
        if url == "bad":
            raise RuntimeError("download failed: bad")
        return f"page {url}"

    return fetch_page, log


class TestFetchAllInOrder(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_all_returns_pages_in_input_order_not_finishing_order(self):
        fetch_page, _ = fake_fetcher()
        self.assertEqual(await fetch_all(["a", "b", "c"], fetch_page), ["page a", "page b", "page c"])

    async def test_fetch_all_starts_every_download_before_any_finishes(self):
        fetch_page, log = fake_fetcher()
        await fetch_all(["a", "b", "c"], fetch_page)
        self.assertEqual(log[:3], ["start a", "start b", "start c"])

    async def test_fetch_all_fails_on_failure_but_other_downloads_keep_running(self):
        fetch_page, log = fake_fetcher()
        with self.assertRaises(RuntimeError) as cm:
            await fetch_all(["slow", "bad"], fetch_page)
        self.assertEqual(str(cm.exception), "download failed: bad")
        self.assertNotIn("end slow", log, "fails as soon as one download fails")
        await asyncio.sleep(0.05)
        self.assertIn("end slow", log, "the slow download still finished")

    async def test_fetch_one_by_one_runs_downloads_strictly_one_after_another(self):
        fetch_page, log = fake_fetcher()
        self.assertEqual(await fetch_one_by_one(["a", "b", "c"], fetch_page), ["page a", "page b", "page c"])
        self.assertEqual(log, ["start a", "end a", "start b", "end b", "start c", "end c"])

    async def test_fetch_one_by_one_stops_at_the_first_failure(self):
        fetch_page, log = fake_fetcher()
        with self.assertRaises(RuntimeError) as cm:
            await fetch_one_by_one(["b", "bad", "c"], fetch_page)
        self.assertEqual(str(cm.exception), "download failed: bad")
        await asyncio.sleep(0.03)
        self.assertEqual(log, ["start b", "end b", "start bad", "end bad"])

    async def test_empty_list_gives_an_empty_list_without_fetching(self):
        fetch_page, log = fake_fetcher()
        self.assertEqual(await fetch_all([], fetch_page), [])
        self.assertEqual(await fetch_one_by_one([], fetch_page), [])
        self.assertEqual(log, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
