import asyncio
import unittest
from unittest import mock

from opds_abs.utils import cache_utils


class TestCacheUtils(unittest.TestCase):
    def setUp(self):
        # Ensure cache persistence is disabled during tests to avoid disk writes
        cache_utils.CACHE_PERSISTENCE_ENABLED = False
        cache_utils._cache.clear()

    def tearDown(self):
        cache_utils._cache.clear()

    def test_cache_set_get_clear(self):
        cache_utils.cache_set("key1", "value1")
        self.assertEqual(cache_utils.cache_get("key1"), "value1")

        # Ensure clear_cache removes the item
        cleared = cache_utils.clear_cache()
        self.assertEqual(cleared, 1)
        self.assertIsNone(cache_utils.cache_get("key1"))

    def test_cache_expiry_removes_item(self):
        # Use a deterministic time source to force expiry
        with mock.patch("opds_abs.utils.cache_utils.time") as mock_time:
            # Time values used by cache_set and cache_get
            # cache_set will call time() once (timestamp)
            # cache_get will call time() once.
            mock_time.time.side_effect = [1.0, 2.0]

            cache_utils.cache_set("key_exp", "value_exp")
            # max_age 0 forces immediate expiry based on the elapsed time (2.0 - 1.0)
            self.assertIsNone(cache_utils.cache_get("key_exp", max_age=0))

    def test_cached_decorator_caches_result(self):
        call_count = {"count": 0}

        @cache_utils.cached(expiry=60)
        async def expensive_compute(x):
            call_count["count"] += 1
            return x * 2

        result1 = asyncio.run(expensive_compute(2))
        result2 = asyncio.run(expensive_compute(2))

        self.assertEqual(result1, 4)
        self.assertEqual(result2, 4)
        self.assertEqual(call_count["count"], 1)
