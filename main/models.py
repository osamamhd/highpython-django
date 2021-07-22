from django.core.files import File
from django.db import models
from django.urls import reverse

from io import BytesIO
from PIL import Image

from autoslug import AutoSlugField
from ai_django_core.models import CommonInfo
from taggit.managers import TaggableManager

localhost = 'http://127.0.0.1:8000'
STATUS_CHOICES = [('Published', 'PUBLISHED'), ('Drafted', 'DRAFTED')]


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='title', unique_with='description')
    description = models.CharField(max_length=300, blank=True)
    cover = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_cover(self):
        if self.cover:
            return localhost + self.cover.url
        return ''

    def articles_count(self):
        return Article.objects.filter(category=self.pk).count()

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Article(CommonInfo, models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique_with='created_at')
    description = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/covers', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', blank=True, null=True)
    content = models.FileField(upload_to='uploads/content/', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default='Drafted')
    like = models.PositiveSmallIntegerField(default=0)
    heart = models.PositiveSmallIntegerField(default=0)
    happy = models.PositiveSmallIntegerField(default=0)
    tags = TaggableManager()

    def get_absolute_url(self):
        return f'{self.category.slug}/{self.slug}/'

    def creation_date(self):
        return self.created_at.strftime('%b %d, %y')

    def get_image(self):
        if self.image:
            return localhost + self.image.url
        return ''

    def get_content_file(self):
        if self.content:
            return localhost + self.content.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return localhost + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return localhost + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(400, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Comment(models.Model):
    author = models.CharField(max_length=50)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="comments")
    text = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

    def creation_date(self):
        return self.created_at.strftime('%b %d, %y')

