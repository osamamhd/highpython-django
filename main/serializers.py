from rest_framework import serializers
from .models import Article
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ['id',
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
                  'content'
                  ]
