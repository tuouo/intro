import markdown
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views import generic
from markdown.extensions.toc import TocExtension # For Chinese(toc)

from comments.forms import CommentForm
from blog.models import Article, Category, Tag

PAGINATE_BY = 7

class PaginateView(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        paginator_date = gen_pagination_data(paginator, page, is_paginated)
        context.update(paginator_date)
        return context

class ArticleListView(PaginateView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = PAGINATE_BY
    model = Article

class ArticleArchivesView(PaginateView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return Article.objects.filter(
                create_at__year=self.kwargs.get('year'),
                create_at__month=self.kwargs.get('month')
            )

class ArticleAuthorView(PaginateView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs.get('pk'))
        # return Article.objects.filter(author_id=self.kwargs.get('pk'))
        return Article.objects.filter(author=author)

class ArticleCategoryView(PaginateView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = PAGINATE_BY
    # model = Article

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # return super(ArticleCategoryView, self).get_queryset().filter(
        #         category=cate).order_by('-create_at')
        return Article.objects.filter(category=cate)

class ArticleTagView(PaginateView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return Article.objects.filter(tags=tag)

class ArticleDetailView(generic.DetailView):
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    model = Article

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_browse()
        return response

    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object(queryset=None)
        # article.body = markdown.markdown(
        #     article.body,
        #     extensions=[
        #         'markdown.extensions.extra',
        #         'markdown.extensions.codehilite',
        #         'markdown.extensions.toc',
        #     ]
        # )
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
            ])
        article.body = md.convert(article.body)
        article.toc = md.toc
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context

def search(request):
    # for self search not haystack
    template_name = 'blog/article_search.html'
    q = request.GET.get('q')
    if not q:
        return render(request, template_name, {'error_msg': "请输入查询关键字"})
    article_list = Article.objects.\
            filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request, template_name,
                  {'error_msg': '', 'article_list': article_list})


def gen_pagination_data(paginator, page, is_paginated, adjoin_num=2):
    if not is_paginated:
        return {}
    page_range = paginator.page_range
    page_num, total_pages = page.number, paginator.num_pages
    show_first, show_last, is_left_more, is_right_more = [False] * 4
    left_start = page_num - 1 - adjoin_num
    left = page_range[left_start if left_start > 0 else 0: page_num - 1]
    right = page_range[page_num:page_num + adjoin_num]

    if page_num != 1:
        if left[0] > 1:
            show_first = True
            if left[0] > 2:
                is_left_more = True
    if page_num != total_pages:
        if right[-1] < total_pages:
            show_last = True
            if right[-1] <  total_pages - 1:
                is_right_more = True
    data = {
        'left': left, 'right': right,
        'show_first': show_first, 'show_last': show_last,
        'is_left_more': is_left_more, 'is_right_more': is_right_more,
    }
    return data

