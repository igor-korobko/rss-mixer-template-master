from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from mem_models import UrlsList, PostList
from tasks import parse


def rss(request):

    urls_list = UrlsList()
    error = ""
    if "add_feed" in request.POST and "feed" in request.POST:
        validator = URLValidator()
        try:
            validator(request.POST["feed"])
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