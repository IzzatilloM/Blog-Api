from django.urls import path
from .models import *
from .views import *

urlpatterns = [
    # path('articles/', ArticleListAPIView.as_view()),
    path('articles/', ArticlesAPIView.as_view()),
    path('articles/<int:pk>/', ArticleRetrieveAPIView.as_view()),
    path('articles/create', ArticleCreateAPIView.as_view()),
    path('articles/mine/', MyArticleAPIView.as_view()),
]