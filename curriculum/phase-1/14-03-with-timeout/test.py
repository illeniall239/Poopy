import asyncio
import time
import unittest

from solution import sleep, with_timeout


async def after(ms, value):
    await sleep(ms)
    return value


class TestWithTimeout(unittest.IsolatedAsyncioTestCase):
    async def test_sleep_returns_none_after_the_delay(self):
        started = time.perf_counter()
        result = await sleep(20)
        self.assertIsNone(result)
        self.assertGreaterEqual(time.perf_counter() - started, 0.015)

    async def test_returns_the_value_when_the_awaitable_is_fast_enough(self):
        self.assertEqual(await with_timeout(after(5, "done"), 50), "done")

    async def test_raises_a_timeout_error_when_the_awaitable_is_too_slow(self):
        with self.assertRaises(TimeoutError) as cm:
            await with_timeout(after(50, "late"), 10)
        self.assertEqual(str(cm.exception), "Timed out after 10ms")

    async def test_does_not_wait_for_the_slow_awaitable_after_timing_out(self):
        started = time.perf_counter()
        with self.assertRaises(TimeoutError):
            await with_timeout(after(50, "late"), 5)
        self.assertLess(time.perf_counter() - started, 0.04, "should fail after about 5ms")

    async def test_passes_through_the_original_error(self):
        boom = RuntimeError("boom")

        async def fail():
            raise boom

        with self.assertRaises(RuntimeError) as cm:
            await with_timeout(fail(), 50)
        self.assertIs(cm.exception, boom)

    async def test_an_already_finished_future_wins_even_with_a_0ms_timeout(self):
        ready = asyncio.get_running_loop().create_future()
        ready.set_result("ready")
        self.assertEqual(await with_timeout(ready, 0), "ready")

    async def test_a_late_error_after_the_timeout_is_ignored(self):
        async def late():
            await sleep(20)
            raise RuntimeError("late failure")

        with self.assertRaises(TimeoutError) as cm:
            await with_timeout(late(), 5)
        self.assertEqual(str(cm.exception), "Timed out after 5ms")
        await sleep(40)

    async def test_negative_ms_raises_a_value_error(self):
        with self.assertRaises(ValueError) as cm:
            await with_timeout(after(0, "x"), -1)
        self.assertEqual(str(cm.exception), "ms must not be negative")


if __name__ == "__main__":
    unittest.main(verbosity=2)
