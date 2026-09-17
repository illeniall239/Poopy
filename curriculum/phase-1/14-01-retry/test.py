import asyncio
import time
import unittest

from solution import retry


def flaky_task(failures):
    """Return (task, errors): task fails `failures` times with a new error each time, then returns "ok"."""
    errors = []

    async def task():
        await asyncio.sleep(0.001)
        if len(errors) < failures:
            error = RuntimeError(f"failure {len(errors) + 1}")
            errors.append(error)
            raise error
        return "ok"

    return task, errors


class TestRetry(unittest.IsolatedAsyncioTestCase):
    async def test_resolves_on_the_first_try_without_retrying(self):
        calls = []

        async def task():
            calls.append(1)
            return "first"

        self.assertEqual(await retry(task, 5), "first")
        self.assertEqual(len(calls), 1)

    async def test_retries_after_failures_until_one_succeeds(self):
        task, errors = flaky_task(2)
        self.assertEqual(await retry(task, 3), "ok")
        self.assertEqual(len(errors), 2)

    async def test_raises_the_last_attempts_error_when_every_attempt_fails(self):
        task, errors = flaky_task(10)
        with self.assertRaises(RuntimeError) as cm:
            await retry(task, 3)
        self.assertIs(cm.exception, errors[2])
        self.assertEqual(len(errors), 3)

    async def test_one_attempt_means_no_retries(self):
        task, errors = flaky_task(1)
        with self.assertRaises(RuntimeError) as cm:
            await retry(task, 1)
        self.assertEqual(str(cm.exception), "failure 1")
        self.assertEqual(len(errors), 1)

    async def test_max_attempts_below_1_raises_value_error_and_never_calls_the_task(self):
        calls = []

        async def task():
            calls.append(1)
            return "x"

        with self.assertRaises(ValueError) as cm:
            await retry(task, 0)
        self.assertEqual(str(cm.exception), "max_attempts must be at least 1")
        with self.assertRaises(ValueError):
            await retry(task, -2)
        self.assertEqual(len(calls), 0)

    async def test_attempts_never_overlap(self):
        state = {"running": 0, "max_running": 0, "calls": 0}

        async def task():
            state["running"] += 1
            state["max_running"] = max(state["max_running"], state["running"])
            state["calls"] += 1
            await asyncio.sleep(0.005)
            state["running"] -= 1
            if state["calls"] < 4:
                raise RuntimeError("not yet")
            return "done"

        self.assertEqual(await retry(task, 4), "done")
        self.assertEqual(state["max_running"], 1)

    async def test_waits_delay_ms_between_attempts(self):
        task, _ = flaky_task(10)
        started = time.perf_counter()
        with self.assertRaises(RuntimeError):
            await retry(task, 3, 25)
        self.assertGreaterEqual(time.perf_counter() - started, 0.04, "expected two waits of about 25ms")


if __name__ == "__main__":
    unittest.main(verbosity=2)
