from .models import Article, Claim, Source, User
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

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

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    created = serializers.DateTimeField(required=True)
    updated = serializers.DateTimeField(required=True)
    deleted = serializers.DateTimeField(allow_null=True, default=None)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user["password"] = make_password(user["password"])
        return user

    def validate_password(self, password):
        return check_password(password, self.password)
