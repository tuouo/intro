from django import template
from django.db.models.aggregates import Count
from django.db.models.functions import TruncMonth

from blog.models import Article, Category, Tag

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-create_at')[:num]

@register.simple_tag
def archives():
    # return Article.objects.dates('create_at', 'month', order='DESC')
    return Article.objects.annotate(date=TruncMonth('create_at')).\
            values('date').annotate(num_article=Count('id')).order_by()

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_article=Count('article')).\
            filter(num_article__gt=0)

@register.simple_tag
def get_tags():
   return Tag.objects.annotate(num_article=Count('article')).\
           filter(num_article__gt=0)
