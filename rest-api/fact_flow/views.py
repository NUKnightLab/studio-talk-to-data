from .models import User, Article, Claim, Source
from .serializers import UserSerializer, ArticleSerializer, ClaimSerializer, SourceSerializer
from .process_article import get_all_claims
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer

    @detail_route(methods=['post'])
    def validate_password(self, request, pk=None):
        user = self.get_object()
        if 'password' in request.data:
            verdict = user.validate_password(request.data['password'])     
            return Response({'is_validated': verdict })

    @detail_route(methods=['post'])
    def update_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.update(user, request.data)
            return Response({ 'status': 'password set' })
        else:
            return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        user = self.get_object() 
        article_serializer = ArticleSerializer(data = request.data)
        if article_serializer.is_valid():
            article_serializer.save()
            claims = get_all_claims(article_serializer.data)
            claim_serializer = ClaimSerializer(data = claims, many = True)

            if claim_serializer.is_valid():
                claim_serializer.save()
                return Response({
                    'article': article_serializer.data,
                    'claims': claim_serializer.data
                })
            else: 
                return Response(
                serializer.errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created')
    serializer_class = ArticleSerializer

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all().order_by('-created')
    serializer_class = ClaimSerializer

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by('-created')
    serializer_class = SourceSerializer