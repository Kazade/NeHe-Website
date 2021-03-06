import os
import logging

from django.core.cache import cache
from articles.models import Article, MenuBlock
from articles.globs import ArticleType
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.cache import cache_page

from .utils import generate_cache_key

@cache_page(60)
def homepage(request):
    try:
        page = int(request.GET.get('page', 0))
    except (TypeError, ValueError):
        page = 0

    NUM_NEWS_PAGES_TO_KEEP = 5
    HOME_PAGE_CACHE_KEY = generate_cache_key(request, [ "page" ])

    #If a page was specified, add it to the cache key
    if page and page <= NUM_NEWS_PAGES_TO_KEEP:
        HOME_PAGE_CACHE_KEY += "_%d" % page
    elif page > NUM_NEWS_PAGES_TO_KEEP:
        raise Http404("We don't allow access to old pages :(")

    #Try to get from the cache
    subs = cache.get(HOME_PAGE_CACHE_KEY)
    if not subs:
        logging.info("Caching with key: %s" % HOME_PAGE_CACHE_KEY)
        #otherwise, hit the datastore :(
        subs = {}

        page_start = page * 10
        page_end = int(page_start + 10)

        logging.info("Rebuilding the homepage cache")

        posts = Article.objects.filter(article_type=ArticleType.NEWS, published=True).order_by('-created_time')[page_start:page_end]

        if not len(posts) and page != 0:
            logging.info("No posts for this page, redirecting...")
            return HttpResponseRedirect("/")

        subs["news_posts"] = {
            "object_list" : posts,
            "next_page_number" : page + 1,
            "has_next" : bool(page < NUM_NEWS_PAGES_TO_KEEP)
        }

        subs["menu_blocks"] = MenuBlock.objects.filter(active=True).order_by('active','-priority').all()

        #24 hours!
        cache.set(HOME_PAGE_CACHE_KEY, subs, 60 * 60 * 24 * 7)

    #FIXME: It will reduce CPU if we store the HTML instead of subs in the cache
    return render_to_response("public/homepage.html", subs, context_instance=RequestContext(request))

@cache_page(60)
def view_article(request, article_id):
    cache_key = generate_cache_key(request)

    subs = cache.get(cache_key)
    if not subs:
        logging.info("Caching with key %s", cache_key)

        article = get_object_or_404(Article, pk=article_id)

        if not article.published:
            raise Http404("This article is not published")

        subs = {}
        subs["article"] = article
        subs["title"] = article.title
        subs["author_profile"] = article.author.profile
        subs["author_name"] = " ".join([article.author.first_name, article.author.last_name])
        cache.set(cache_key, subs, 60 * 60 * 24 * 7)

    return render_to_response("public/view_article.html", subs, context_instance=RequestContext(request))

@cache_page(60)
def view_listing(request, listing_id):
    cache_key = generate_cache_key(request)

    subs = cache.get(cache_key)
    if not subs:
        logging.info("Caching with key %s", cache_key)

        listing = get_object_or_404(ArticleListing, pk=listing_id)

        subs = {
            "articles" : []
        }

        for article_id in listing.articles:
            article = Article.objects.get(pk=article_id)
            subs["articles"].append(article)

        subs["title"] = listing.title
        cache.set(cache_key, subs, 60 * 60 * 24 * 7)
    return render_to_response("public/view_listing.html", subs, context_instance=RequestContext(request))

#Cache the page for 24 hours
@cache_page(60 * 60 * 24)
def article_listing(request, kind, page):
    logging.info("Processing article_listing page %s %s", str(kind), str(page))
    articles = Article.get_by_kind(kind).order_by('original_id')
    pages = Paginator(articles, 5)
    subs = {}
    try:
        subs['articles'] = pages.page(int(page))
    except (PageNotAnInteger, TypeError):
        subs['articles'] = pages.page(1)
    except EmptyPage:
        subs['articles'] = pages.page(pages.num_pages)

    subs["title"] = "Articles %i - %i" % (subs['articles'].start_index(), subs['articles'].end_index())
    return render_to_response("public/article_listing.html", subs)

def legacy_tutorial_redirect(request):
    old_lesson_id = request.GET.get('lesson', None)
    if old_lesson_id is None:
        raise Http404("Invalid old lesson id")

    try:
        old_lesson_id = int(old_lesson_id)
    except (ValueError, TypeError):
        raise Http404("Invalid id")


    #Generate a cache key for the redirect
    cache_key = generate_cache_key(request, ["lesson"])

    #If the redirect url is in the cache, use it
    result = cache.get(cache_key)
    if result:
        return HttpResponsePermanentRedirect(result)

    #otherwise calc the redirect url, store it in the cache and return it
    new_article = get_object_or_404(Article, original_id=old_lesson_id, article_type="TUTORIAL")

    redirect_url = new_article.get_absolute_url()
    cache.set(cache_key, redirect_url, 60 * 60 * 24)

    return HttpResponsePermanentRedirect(redirect_url)

def legacy_article_redirect(request):
    old_article_id = request.GET.get('article', None)
    if old_article_id is None:
        raise Http404("Invalid old article id")

    try:
        old_article_id = int(old_article_id)
    except (ValueError, TypeError):
        raise Http404("Invalid id")

    cache_key = generate_cache_key(request, ["article"])
    result = cache.get(cache_key)
    if result:
        return HttpResponsePermanentRedirect(result)

    new_article = get_object_or_404(Article, original_id=old_article_id, article_type="ARTICLE")

    redirect_url = new_article.get_absolute_url()
    cache.set(cache_key, redirect_url, 60 * 60 * 24)

    return HttpResponsePermanentRedirect(redirect_url)

@cache_page(60*60*24*7)
def legacy_data_redirect(request, url):
    logging.debug("Working out data URL for %s", url)
    return HttpResponsePermanentRedirect(os.path.join(settings.UPLOADED_CONTENT_BASE_URL, "data", url))

#Cache the page for 24 hours
@cache_page(60 * 60 * 24)
def legacy_index_page_redirect(request):
    try:
        index = int(request.GET.get("index"))
    except (TypeError, ValueError):
        raise Http404("Invalid index")

    LOOKUP = {
        1 : "/tutorial/lessons_01__05/22004/",
        2 : "/tutorial/lessons_06__10/17010/",
        3 : "/tutorial/lessons_11__15/28001/",
        4 : "/tutorial/lessons_16__20/28002/",
        5 : "/tutorial/lessons_21__25/25009/",
        6 : "/tutorial/lessons_26__30/29002/",
        7 : "/tutorial/lessons_31__35/25010/",
        8 : "/tutorial/lessons_36__40/19005/",
        9 : "/tutorial/lessons_41__45/28003/",
        10: "/tutorial/lessons_46__48/16016/",
    }

    if index not in LOOKUP:
        return Http404()

    return HttpResponsePermanentRedirect(LOOKUP[index])

def fix_relative_urls(data):
    import re
    regex = 'href="(?P<url>(?!/).{1}(.+?))"'
    result = re.search(regex, data)
    while result:
        m = result.group('url')
        print("Replacing: " + m)
        data = data.replace(m, '/data/lessons/' + m)
        result = re.search(regex, data)

    return data.replace('/data/lessons/mailto:', 'mailto:')

def submit_news(request):
    pass
