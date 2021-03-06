#!/usr/bin/env python
from articles.models import Article

def update_article_types():
    for article in Article.objects.all():
        if article.article_type: continue
        
        new_type = article.kind.description
        assert new_type in ("NEWS", "TUTORIAL", "ARTICLE")
        article.article_type = new_type
        article.save()
        
        
