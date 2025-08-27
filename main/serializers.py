from rest_framework import serializers
from .models import *

class ArticleSafeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='get_full_name', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

        extra_kwargs = {
            'author':{'read_only':True},
        }