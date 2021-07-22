from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    LatestArticlesList,
    CategoriesListView,
    CategoryDetailView,
    CommentCreateListAPIView,
    article_heart,
    article_happy,
    article_like,
    )

urlpatterns = [
    path('<int:article_pk>/comments/', CommentCreateListAPIView.as_view()),
    path('<int:pk>/heart/', article_heart),
    path('<int:pk>/happy/', article_happy),
    path('<int:pk>/like/', article_like),
    path('latest-articles/', LatestArticlesList.as_view()),
    path('', ArticleListView.as_view()),
    path('<slug:category_slug>/<slug:article_slug>/', ArticleDetailView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('<slug:category_slug>/', CategoryDetailView.as_view()),
]
