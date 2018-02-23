from django.contrib.auth.models import User, Group
from rest_framework import serializers
from datetime import datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ArticleSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    created = serializers.DateTimeField(required=True)
    updated = serializers.DateTimeField(required=True)
    deleted = serializers.DateTimeField(allow_null=True, default=None)
    text = serializers.CharField(required=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.updated = datetime.now()
        instance.save()
        return instance 
