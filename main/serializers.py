from rest_framework import serializers
from .models import Article, Category, Comment
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = [
          'id',
          'category',
          'created_by',
          'title',
          'slug',
          'description',
          'heart',
          'like',
          'happy',
          'tags',
          'creation_date',
          'get_image',
          'get_thumbnail',
          'get_absolute_url',
          'get_content_file'
        ]


class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'get_cover',
            'articles_count',
            'get_absolute_url',
            'articles'
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'text',
            'article',
            'creation_date'
        ]
        read_only_fields = ['article']

