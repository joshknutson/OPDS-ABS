import unittest
from unittest import mock

from opds_abs.utils import cache_utils


class TestCacheApiHelpers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure cache persistence is disabled during tests to avoid disk writes
        cache_utils.CACHE_PERSISTENCE_ENABLED = False
        cache_utils._cache.clear()
        cache_utils._last_save_time = 0

    def tearDown(self):
        cache_utils._cache.clear()
        cache_utils._last_save_time = 0

    async def test_get_cached_library_items_caches_results(self):
        fetch_from_api = mock.AsyncMock(return_value={"items": [{"id": "1"}]})
        filter_items = lambda data: data["items"]

        result1 = await cache_utils.get_cached_library_items(
            fetch_from_api, filter_items, "user", "lib1"
        )
        result2 = await cache_utils.get_cached_library_items(
            fetch_from_api, filter_items, "user", "lib1"
        )

        self.assertEqual(result1, result2)
        self.assertEqual(fetch_from_api.call_count, 1)

    async def test_get_cached_library_items_bypass_cache(self):
        fetch_from_api = mock.AsyncMock(side_effect=[
            {"items": [{"id": "1"}]},
            {"items": [{"id": "2"}]},
        ])
        filter_items = lambda data: data["items"]

        result1 = await cache_utils.get_cached_library_items(
            fetch_from_api, filter_items, "user", "lib1", bypass_cache=True
        )
        result2 = await cache_utils.get_cached_library_items(
            fetch_from_api, filter_items, "user", "lib1", bypass_cache=True
        )

        self.assertNotEqual(result1, result2)
        self.assertEqual(fetch_from_api.call_count, 2)

    async def test_get_cached_search_results_caches_results(self):
        fetch_from_api = mock.AsyncMock(return_value={"results": [1]})

        result1 = await cache_utils.get_cached_search_results(
            fetch_from_api, "user", "lib1", "query"
        )
        result2 = await cache_utils.get_cached_search_results(
            fetch_from_api, "user", "lib1", "query"
        )

        self.assertEqual(result1, result2)
        self.assertEqual(fetch_from_api.call_count, 1)

    async def test_get_cached_series_details_caches_results(self):
        series_id = "series1"
        fetch_from_api = mock.AsyncMock(return_value={"results": [{"id": series_id, "name": "Series"}]})

        result1 = await cache_utils.get_cached_series_details(
            fetch_from_api, "user", "lib1", series_id
        )
        result2 = await cache_utils.get_cached_series_details(
            fetch_from_api, "user", "lib1", series_id
        )

        self.assertEqual(result1, result2)
        self.assertEqual(fetch_from_api.call_count, 1)

    async def test_get_cached_author_details_caches_results(self):
        library_items = [
            {"media": {"ebookFile": "file", "metadata": {"authorName": "Author A"}}},
            {"media": {"ebookFormat": "epub", "metadata": {"authorName": "Author A"}}},
            {"media": {"ebookFile": "file", "metadata": {"authorName": "Author B"}}},
        ]

        async def fake_get_cached_library_items(
            fetch_func, filter_func, username, library_id, token=None, bypass_cache=False
        ):
            return library_items

        with mock.patch(
            "opds_abs.utils.cache_utils.get_cached_library_items",
            side_effect=fake_get_cached_library_items,
        ):
            fetch_authors = mock.AsyncMock(return_value={
                "authors": [
                    {"name": "Author A", "id": "a1", "imagePath": "pathA"},
                    {"name": "Author B", "id": "b1", "imagePath": "pathB"},
                ]
            })

            # filter_func is not used due to patching get_cached_library_items
            result1 = await cache_utils.get_cached_author_details(
                fetch_authors, lambda data: data, "user", "lib1"
            )
            result2 = await cache_utils.get_cached_author_details(
                fetch_authors, lambda data: data, "user", "lib1"
            )

            self.assertEqual(fetch_authors.call_count, 1)

            authors_by_name = {a["name"]: a for a in result1}
            self.assertEqual(authors_by_name["Author A"]["ebook_count"], 2)
            self.assertEqual(authors_by_name["Author A"]["id"], "a1")
            self.assertEqual(authors_by_name["Author B"]["ebook_count"], 1)
            self.assertEqual(authors_by_name["Author B"]["imagePath"], "pathB")

    async def test_get_cached_series_items_caches_results(self):
        series_id = "series1"
        fetch_from_api = mock.AsyncMock(return_value={"results": [{"id": "1"}]})
        filter_items = lambda data: data["results"]

        result1 = await cache_utils.get_cached_series_items(
            fetch_from_api, filter_items, "user", "lib1", series_id
        )
        result2 = await cache_utils.get_cached_series_items(
            fetch_from_api, filter_items, "user", "lib1", series_id
        )

        self.assertEqual(result1, result2)
        self.assertEqual(fetch_from_api.call_count, 1)
