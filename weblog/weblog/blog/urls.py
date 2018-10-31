from django.urls import path, re_path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    re_path('archives/(?P<year>[0-9]{4})/(?P<month>1[0-2]|[1-9])',
        views.ArticleArchivesView.as_view(), name='article_archives'),
    path('category/<int:pk>/',
        views.ArticleCategoryView.as_view(), name='article_category'),
    path('tag/<int:pk>/', views.ArticleTagView.as_view(), name='article_tag'),
    re_path('author/(?P<pk>\d+)/',
        views.ArticleAuthorView.as_view(), name='article_author'),
    path('search/', views.search, name='search'),
]

