from django.test import TestCase
from mixer.mem_models import UrlsList, PostList, Post
from django.core.cache import cache


class UrlsListTest(TestCase):

    url = 'http://feeds.bbci.co.uk/news/rss.xml'
    cache_urls_name = "urls"

    def setUp(self):
        self.urls = UrlsList()

    def tearDown(self):
        cache.delete(self.cache_urls_name)

    def test_add_url(self):
        len_before = len(self.urls.urls)
        self.urls.add_url(self.url)
        self.assertEqual(len(self.urls.urls), len_before + 1)

    def test_del_url(self):
        len_before = len(self.urls.urls)
        item_id = self.urls.add_url(self.url)
        self.urls.del_url(item_id)
        self.assertEqual(len(self.urls.urls), len_before)

    def test_urls_update_cache_on_destroy(self):
        self.urls.add_url(self.url)
        del self.urls
        self.assertNotEqual(cache.get(self.cache_urls_name), None)

    def test_get_urls_return_dict_of_urls(self):
        len_before = len(self.urls.urls)
        self.urls.add_url(self.url)
        test_list = self.urls.get_urls()
        self.assertIsInstance(test_list, dict)
        self.assertEqual(len_before + 1, len(test_list.values()))


class PostListTests(TestCase):

    cache_post_name = "posts"

    def setUp(self):
        self.posts = PostList()

    def tearDown(self):
        cache.delete(self.cache_post_name)

    def test_posts_update_cache_on_object_destroy(self):
        post = Post(1, "author", "title", "summary", "content", "pub_date", "chanel_title", "chanel_link")
        self.posts.add_post(post)
        del self.posts
        self.assertNotEqual(cache.get(self.cache_post_name), None)

    def test_add_post(self):
        post = Post(1, "author", "title", "summary", "content", "pub_date", "chanel_title", "chanel_link")
        self.posts.add_post(post)
        self.assertEqual(len(self.posts.posts), 1)


class PostTests(TestCase):

    def test_post_structure(self):
        keys = ['channel_title', 'title', 'channel_link', 'author', 'summary', 'content', 'pub_date', 'id']
        for key in keys:
            self.assertTrue(key in Post.__dict__.keys())








