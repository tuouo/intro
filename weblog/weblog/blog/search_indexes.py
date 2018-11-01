import datetime
from haystack import indexes
from blog.models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    author = indexes.CharField(model_attr='author')
    create_at = indexes.CharField(model_attr='create_at')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.\
                filter(create_at__lte=datetime.datetime.now())

