from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer
from .models import Article, Category


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
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
