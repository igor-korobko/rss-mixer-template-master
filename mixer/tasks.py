from mem_models import Post, PostList
import feedparser


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