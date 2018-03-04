from .models import User, Article
from .serializers import UserSerializer, ArticleSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created')
    serializer_class = ArticleSerializer
    