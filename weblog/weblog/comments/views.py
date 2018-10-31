from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article
from comments.models import Comment
from comments.forms import CommentForm

def article_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():  # auto checked by django
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect(article)
        else:
            comment_list = article.comment_set.all()
            context = {'article': article, 'form': form, 'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)

    return redirect(article)

