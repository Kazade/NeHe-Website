'''
Created on 19 Jun 2011

@author: lukeb
'''

from django.contrib import admin
from articles.models import MenuBlock, MenuGroup, Article, ArticleListing, Link, UserProfile

class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "/static/js/syntax_highlighter/shCore.js",
            "/static/js/syntax_highlighter/shBrushJScript.js",
            "/static/css/syntax_highlighter/shCoreDefault.css",
            "/static/js/tiny_mce/tiny_mce.js",
            "/static/js/init_admin.js"
        )

    exclude = (
        "kind",
        "comments_enabled",
        "tooltip_html"
    )

admin.site.register(MenuBlock)
admin.site.register(MenuGroup)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleListing)
admin.site.register(Link)
admin.site.register(UserProfile)
