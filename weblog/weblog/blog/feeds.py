from django.contrib.syndication.views import Feed

from blog.models import Article

class ArticleAllRssFeed(Feed):
    title = "Leaf on the wind"
    link = '/'  # default url for show
    description = 'Learning experience & personal code info'

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return "[{}] {}".format(item.category, item.title)

    def item_description(self, item):
        return item.body

