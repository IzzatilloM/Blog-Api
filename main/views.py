from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .serializers import *

# class ArticleListAPIView(ListAPIView):
#     serializer_class = ArticleSafeSerializer
#     queryset = Article.objects.filter(published=True)

class ArticlesAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                description='Search by title or context',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='published',
                description='Filter by published status',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                name='ordering',
                description='Ordering by title, created_at, views (asc, desc)',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['title','created_at','views', '-title', '-created_at', '-views'],
            )
        ]
    )
    def get(self, request):
        articles = Article.objects.all()

        published = request.GET.get('published')
        if published:
            if published.lower() == 'true':
                articles = articles.filter(published=True)
            elif published.lower() == 'false':
                articles = articles.filter(published=False)

        search = request.GET.get('search')
        if search:
            articles = articles.filter(Q(title__icontains=search) | Q(context__icontains=search))

            ordering = request.GET.get('ordering')
            if ordering:
                try:
                    articles = articles.order_by(ordering)
                except Exception as e:
                    return Response(
                        {
                            'succes':False,
                            'error':'Ordering only by title, created_at, views with (asc, desc)'
                        },
                        status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSafeSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleRetrieveAPIView(RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset =  Article.objects.filter(published=True)

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if self.request.user != article.author:
            article.views += 1
            article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)

# class ArticleCreateAPIView(CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all() 
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)




class ArticleCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=ArticleSerializer
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyArticleAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )

    serializer_class = ArticleSerializer
    queryset =  Article.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'context']
    ordering_fields = ['title','created_at','views']



    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['title','created_at','views', '-title', '-created_at', '-views'],
                description='Ordering by title, views, created_at (asc,desc)'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        super().get(*args, **kwargs)