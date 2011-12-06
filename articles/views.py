import datetime
from django import forms
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpRequest
from articles.models import Article, ArticleType, MenuGroup
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import resolve, reverse
from django.utils.cache import get_cache_key
from django.core.cache import cache
    
def index(request):
    subs = {}
    subs["news_posts"] = Article.get_by_kind("NEWS")
    return render_to_response("articles/index.html", subs)

@staff_member_required
def admin_article_list(request):
    if request.method == 'POST':
        to_delete = request.POST.getlist('selected_articles')
        for article in to_delete:
            to_delete = Article.objects.get(pk=int(article))
            to_delete.delete()
            
    
    if "query" in request.GET:
        kind_desc = request.GET["query"].upper()
        try:
            articles = Article.get_by_kind(kind_desc)
        except ArticleType.DoesNotExist:
            raise Http404("No such article type")
    else:
        articles = Article.objects
        
    posts = articles.order_by("-created_time")
    article_paginator = Paginator(posts, 30)

    subs = {}

    try:
        page = request.GET.get('page')
        subs["articles"] = article_paginator.page(page)
    except (PageNotAnInteger, TypeError):
        subs["articles"] = article_paginator.page(1)
    except EmptyPage:
        subs["articles"] = article_paginator.page(article_paginator.num_pages)
        
    subs["breadcrumbs"] = [
        { "text" : "Articles", "url" : None }
    ]
    
    subs["article_paginator"] = article_paginator    
    subs["page_heading"] = "Articles"
    
    return render_to_response("articles/admin_article_list.html", subs)

@staff_member_required
def admin_article_type_list(request):
    article_types = ArticleType.objects.all()
    subs = {}
    subs["article_types"] = article_types
    subs["breadcrumbs"] = [
        { "text" : "Article Types", "url" : None}
    ]
    subs["page_heading"] = "Article types"
    return render_to_response("articles/admin_article_type_list.html", subs)

class ArticleTypeForm(forms.ModelForm):
    class Meta(object):
        model = ArticleType

class ArticleForm(forms.ModelForm):
    class Meta(object):
        model = Article

@staff_member_required
def admin_article_create(request):
    subs = {}
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/_admin/article/")
    else:
        form = ArticleForm()

    subs["form"] = form
    subs["breadcrumbs"] = [
        { "text" : "Articles", "url" : "/_admin/article/" },
        { "text" : "Create", "url" : None }
    ]
    subs["page_heading"] = "Create an article"
    return render_to_response("articles/admin_article_create.html", subs)

@staff_member_required
def admin_article_edit(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Invalid article type")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/_admin/article/")
    else:
        form = ArticleForm(instance=article)

    subs = {}
    subs["form"] = form
    subs["breadcrumbs"] = [
        { "text" : "Articles", "url" : "/_admin/article/" },
        { "text" : "Edit %s" % article.title, "url" : None }
    ]
    subs["article"] = article
    
    subs["page_heading"] = "Editing '%s'" % article.title
    return render_to_response("articles/admin_article_edit.html", subs)

@staff_member_required
def admin_article_type_create(request):
    subs = {}
    if request.method == "POST":
        form = ArticleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/_admin/article_type/")
    else:
        form = ArticleTypeForm()

    subs["form"] = form
    subs["breadcrumbs"] = [
        { "text" : "Article Types", "url" : "/_admin/article_type/"},
        { "text" : "Create", "url" : None},
    ]
    subs["page_heading"] = "Create a new article type"
    return render_to_response("articles/admin_article_type_create.html", subs)

@staff_member_required
def admin_article_type_edit(request, article_type_id):
    try:
        article_type = ArticleType.objects.get(pk=article_type_id)
    except ArticleType.DoesNotExist:
        raise Http404("Invalid article type")

    if request.method == "POST":
        form = ArticleTypeForm(request.POST, instance=article_type)
        if form.is_valid():
            form.save()
    else:
        form = ArticleTypeForm(instance=article_type)

    subs = {}
    subs["form"] = form
    subs["breadcrumbs"] = [
        { "text" : "Article Types", "url" : "/_admin/article_type/"},
        { "text" : "Edit %s" % article_type.description, "url" : None},
    ]
    subs["page_heading"] = "Editing '%s'" % article_type.description
    subs["article_type"] = article_type
    return render_to_response("articles/admin_article_type_edit.html", subs)


class CacheClearForm(forms.Form):
    url_to_clear = forms.CharField(max_length=1024, help_text="The URL of the page to clear the cache for")    
    
    def clean_url_to_clear(self):
        url = self.cleaned_data["url_to_clear"]
        try:
            match = resolve(url)
        except Http404:
            raise ValidationError("Unrecognized url!")
            
        return url

def expire_view_cache(view_name, args=None, kwargs=None, namespace=None, key_prefix=None, method="GET"):
    """
    This function allows you to invalidate any view-level cache. 
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namepace: optioal, if an application namespace is needed
        key prefix: for the @cache_page decorator for the function (if any)
    """
    
    args = args or []
    kwargs = kwargs or {}
    
    # create a fake request object
    request = HttpRequest()
    request.method = method
    
    # Lookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args, kwargs=kwargs)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):            
            cache.set(key, None, 0)
        return True
    return False
    
def expire_view_by_url(view_url, key_prefix=None):
    # create a fake request object
    request = HttpRequest()
    request.method = "GET"
    
    request.path = view_url
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):            
            cache.set(key, None, 0)
        return True
    return False


@staff_member_required
def admin_manage_cache(request):
    if request.method == "POST":
        f = CacheClearForm(request.POST)
        if f.is_valid():
            assert expire_view_by_url(f.cleaned_data["url_to_clear"])
    else:
        f = CacheClearForm()
        
    subs = {
        "form" : f
    }            
    
    return render_to_response("articles/admin_manage_cache.html", subs)

@staff_member_required
def admin_home(request):
    subs = {}
    subs['model_types'] = [
        { 'text' : 'Articles', 'url_slug' : 'article'},
        { 'text' : 'Article Types', 'url_slug' : 'article_type'},
        { 'text' : 'Manage Cache', 'url_slug' : 'manage_cache' } 
    ]
    
    subs['breadcrumbs'] = []
    subs["page_heading"] = "Admin Home"
    return render_to_response("articles/admin_home.html", subs)
            
