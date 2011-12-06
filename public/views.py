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

#Cache the page for two weeks
@cache_page(60 * 60 * 24 * 14)
def homepage(request):
    subs = {}
    
    try:
        page = int(request.GET.get('page', 0))
    except (TypeError, ValueError):
        page = 0
        
    page_start = page * 15
    page_end = int(page_start + 15)
    
    posts = Article.objects.filter(article_type=ArticleType.NEWS).filter(published=True).order_by('-created_time')[page_start:page_end]        
        
    subs["news_posts"] = {
        "object_list" : posts,
        "next_page_number" : page + 1,
        "has_next" : True
    }
    

    subs["menu_blocks"] = MenuBlock.objects.filter(active=True).order_by('active','-priority').all()

    return render_to_response("public/homepage.html", subs)

#Cache the page for a week
@cache_page(604800)
def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    if not article.published:
        raise Http404("This article is not published")
    
    subs = {}
    subs["article"] = article
    subs["title"] = article.title
    return render_to_response("public/view_article.html", subs, context_instance=RequestContext(request))

#Cache the page for 10 minutes
@cache_page(604800)
def article_listing(request, kind, page):
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
    cache_key = "LEGACY_TUTORIAL_REDIRECT_CACHE_%s" % old_lesson_id
    
    #If the redirect url is in the cache, use it
    result = cache.get(cache_key)    
    if result:
        return HttpResponsePermanentRedirect(result)
       
    #otherwise calc the redirect url, store it in the cache and return it
    kind = ArticleType.objects.get(description="TUTORIAL")
    new_article = get_object_or_404(Article, original_id=old_lesson_id, kind=kind)
        
    redirect_url = '/tutorial/%s/%i/' % (new_article.url_name(), new_article.pk)
    cache.set(cache_key, redirect_url, 604800)
    
    return HttpResponsePermanentRedirect(redirect_url)

def legacy_article_redirect(request):
    old_article_id = request.GET.get('article', None)
    if old_article_id is None:
        raise Http404("Invalid old article id")
    
    try:
        old_article_id = int(old_article_id)
    except (ValueError, TypeError):
        raise Http404("Invalid id")

    cache_key = "LEGACY_ARTICLE_REDIRECT_CACHE_%s" % old_article_id
    result = cache.get(cache_key)
    if result:
        return HttpResponsePermanentRedirect(result)
        
    kind = ArticleType.objects.get(description="ARTICLE")
    new_article = get_object_or_404(Article, original_id=old_article_id, kind=kind)
    
    redirect_url = '/article/%s/%i/' % (new_article.url_name(), new_article.pk)
    cache.set(cache_key, redirect_url, 604800)
    
    return HttpResponsePermanentRedirect(redirect_url)
        
def legacy_data_redirect(request, url):
    logging.debug("Working out data URL for %s", url)
    return HttpResponsePermanentRedirect(os.path.join(settings.UPLOADED_CONTENT_BASE_URL, "data", url))
  
@cache_page(604800)  
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

    