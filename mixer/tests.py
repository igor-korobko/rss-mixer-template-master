from django.test import TestCase
from mixer.views import UrlsList, PostList, Post
from django.core.cache import cache
import pickle


class UrlsTests(TestCase):

    url = 'http://feeds.bbci.co.uk/news/rss.xml'
    cache_urls_name = "urls"

    def test_cache_save(self):
        cache.delete(self.cache_urls_name)
        urls = UrlsList()
        urls.add_url(self.url)
        del urls
        self.assertNotEqual(cache.get(self.cache_urls_name), None)

    def test_cache_return(self):
        cache.delete(self.cache_urls_name)
        urls = UrlsList()
        urls.add_url(self.url)
        del urls
        urls_obj = pickle.loads(cache.get(self.cache_urls_name))
        self.assertEqual(urls_obj.urls.popitem()[1], self.url)

    def test_get_url_where_urls_is_empty(self):
        cache.delete(self.cache_urls_name)
        urls = UrlsList()
        self.assertIsNone(urls.get_urls())

    def test_add_and_get_url_where_urls_is_not_empty(self):
        cache.delete(self.cache_urls_name)
        urls = UrlsList()
        urls.add_url(self.url)
        self.assertEqual(len(urls.get_urls()), 1)
        self.assertEqual(urls.get_urls().popitem()[1], self.url)

    def test_del_url(self):
        cache.delete(self.cache_urls_name)
        urls = UrlsList()
        urls.add_url(self.url)
        self.assertEqual(len(urls.urls), 1)
        item = {}
        item.update(urls.get_urls())
        item = item.popitem()
        self.assertEqual(item[1], self.url)
        urls.del_url(int(item[0]))
        self.assertEqual(len(urls.urls), 0)
        self.assertIsNone(urls.get_urls())


class PostTests(TestCase):

    cache_post_name = "posts"

    def test_cache_save(self):
        cache.delete(self.cache_post_name)
        urls = PostList()
        del urls
        self.assertNotEqual(cache.get(self.cache_post_name), None)








