from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('core.Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('core.Tag')
    content = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
