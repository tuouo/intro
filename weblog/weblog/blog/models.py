import markdown

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags

class Base(models.Model):
    create_at = models.DateTimeField('create_at', auto_now_add=True)
    modify_at = models.DateTimeField('modify_at', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-create_at']

class Category(Base):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Tag(Base):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = []

class Article(Base):
    author = models.ForeignKey(
            User, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
            Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    browse = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=60)
    excerpt = models.CharField(max_length=200, blank=True)
    body = models.TextField()

    def __str__(self):
        return "{} : {}({})".format(self.title, self.author, self.create_at.date())

    def get_detail_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.pk})

    get_absolute_url = get_detail_url

    def increase_browse(self):
        self.browse += 1
        self.save(update_fields=['browse'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Article, self).save(*args, **kwargs)

