# -*- coding: utf-8 -*-
import time
from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.views.generic import TemplateView
from django.core.cache import cache
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pickle
import feedparser


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


def parse(urls):
    """
     urls = {0: 'http://...', 2: 'http://...', ...}
    """
    post_list = PostList()
    for i in urls.keys():
        feed = feedparser.parse(urls[i])
        for item in feed["items"]:
            posts_count = len(post_list.posts)
            if "author" in item:
                author = item["author"]
            else:
                author = "unanimous"
            post = Post(posts_count,
                        author,
                        item["title"],
                        item["summary"],
                        item["description"],
                        item["published_parsed"],
                        feed["channel"]["title"],
                        feed["channel"]["link"])
            post_list.add_post(post)
    del post_list


class MixerView(TemplateView):
    template_name = 'index.html'


def rss(request):

    urls_list = UrlsList()
    error = ""
    is_url = False
    # raise
    if "add_feed" in request.POST and "feed" in request.POST:
        validator = URLValidator()
        try:
            is_url = validator(request.POST["feed"])
            # raise
        except ValidationError, e:
            error = e

        if error == '':
            urls_list.add_url(request.POST["feed"])


    parse(urls_list.urls)
    post_list = PostList()
    posts = post_list.sorted_posts_out_in_array()

    resp = {'urls': urls_list.urls,
            "urls_count": len(urls_list.urls),
            "post_list": posts,
            "posts_count": len(posts),
            "error": error}
    return render(request, 'index.html', resp)


def del_url(request, url_id):
    urls_list = UrlsList()
    urls_list.del_url(url_id)
    return redirect('rss')