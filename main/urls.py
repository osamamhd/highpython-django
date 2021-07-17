from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    CategoriesListView,
    CategoryDetailView,
    CommentCreateListAPIView,

    )

urlpatterns = [
    path('', ArticleListView.as_view()),
    path('<slug:category_slug>/<slug:article_slug>/', ArticleDetailView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('<slug:category_slug>/', CategoryDetailView.as_view()),
    path('<int:article_pk>/comments/', CommentCreateListAPIView.as_view()),
]
