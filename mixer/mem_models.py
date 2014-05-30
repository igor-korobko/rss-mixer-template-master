from django.core.cache import cache
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pickle
import time


class UrlsList():
    """
    self.urls = {0: 'http://...', 2: 'http://...', ...}
    """
    def __init__(self):
        self.urls = {}
        urls_obj_cache = cache.get("urls")
        if urls_obj_cache is not None:
            obj = pickle.loads(urls_obj_cache)
            self.urls.update(obj.urls)

    def __del__(self):
        data = pickle.dumps(self)
        cache.delete("urls")
        cache.set("urls", data)

    def get_urls(self):
        if len(self.urls)>0:
            return self.urls
        else:
            return None

    def add_url(self, url):
        id = int(time.time())
        self.urls[id] = url

    def del_url(self, key):
        if isinstance(key, int):
            del self.urls[key]
        else:
            del self.urls[int(key)]


class Post():
    id = 0
    author = ''
    title = ''
    summary = ''
    content = ''
    pub_date = ''
    channel_title = ''
    channel_link = ''

    def __init__(self, id_, author, title, summary, content, pub_date, channel_title, channel_link):
        self.id = id_
        self.author = author
        self.title = title
        self.summary = summary
        self.content = content
        self.pub_date = pub_date
        self.channel_title = channel_title
        self.channel_link = channel_link


class PostList():
    def __init__(self):
        self.posts = {}
        posts_obj_cache = cache.get("posts")
        if posts_obj_cache is not None:
            obj = pickle.loads(posts_obj_cache)
            self.posts.update(obj.posts)

    def __del__(self):
        data = pickle.dumps(self)
        cache.delete("posts")
        cache.set("posts", data)

    def compare(self, item):
        flag = False
        for i in range(0, len(self.posts)):
            if item.title == self.posts[i].title \
                    and item.pub_date == self.posts[i].pub_date \
                    and item.channel_title == self.posts[i].channel_title:
                flag = True
        return flag

    def add_post(self, post):
        if isinstance(post, Post):
            post_count = len(self.posts)
            if post_count > 0:
                if self.compare(post):
                    pass
                else:
                    self.posts[post_count] = post
            else:
                self.posts[post_count] = post
        else:
            raise("Is not Post object")

    def sorted_posts_out_in_array(self):
        posts_arr = []
        for id, value in sorted(self.posts.items(), key=lambda x: x[1].pub_date):
            posts_arr.append(value)
        return posts_arr
