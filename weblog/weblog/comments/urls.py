from django.urls import path

from comments import views

app_name = 'comments'
urlpatterns = [
    path('article/<int:article_pk>/', views.article_comment, name='article_comment'),
]
