from django.db import models

class Base(models.Model):
    create_at = models.DateTimeField('create_at', auto_now_add=True)
    modify_at = models.DateTimeField('modify_at', auto_now=True)

    class Meta:
        abstract = True

class Comment(Base):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    article = models.ForeignKey('blog.Article', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-create_at']
