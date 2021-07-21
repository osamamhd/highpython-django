from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view

from django.http import Http404

from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer
from .models import Article, Category


class ArticleListView(APIView):
    def get(self, request, format=None):
        articles = Article.objects.filter(status="Published").select_related()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    def get_object(self, category_slug, article_slug):
        try:
            return Article.objects.filter(category__slug=category_slug).get(slug=article_slug)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, article_slug, format=None):
        articles = self.get_object(category_slug, article_slug)
        serializer = ArticleSerializer(articles)
        return Response(serializer.data)


class CategoriesListView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CommentCreateListAPIView(CreateModelMixin, ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_pk = self.kwargs.get("article_pk", None)
        article = get_object_or_404(Article, pk=article_pk)
        qs = article.comments.all()
        return qs

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        article_pk = self.kwargs.get("article_pk", None)
        article = get_object_or_404(Article, pk=article_pk)
        serializer.save(article=article)


@api_view(['POST'])
def article_heart(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.heart += 1
    article.save()
    data = {
        'success': True
    }
    return Response(data)


@api_view(['POST'])
def article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.like += 1
    article.save()
    data = {
        'success': True
    }
    return Response(data)



@api_view(['POST'])
def article_happy(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.happy += 1
    article.save()
    data = {
        'success': True
    }
    return Response(data)