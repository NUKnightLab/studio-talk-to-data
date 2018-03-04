from .models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer
