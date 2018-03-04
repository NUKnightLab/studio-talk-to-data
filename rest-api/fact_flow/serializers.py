from .models import Article, Claim, Source, User
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class ArticleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    created = serializers.DateTimeField(default=None)
    updated = serializers.DateTimeField(default=None)
    deleted = serializers.DateTimeField(allow_null=True, default=None)
    text = serializers.CharField(required=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.updated = datetime.now()
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=None)
    created = serializers.DateTimeField(default=None)
    updated = serializers.DateTimeField(default=None)
    deleted = serializers.DateTimeField(default=None)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.password = make_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.updated = datetime.now()
        instance.save()
        return instance

class ClaimSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=None)
    article_id = serializers.UUIDField(default=None)
    text = serializers.CharField(required=True)
    created = serializers.DateTimeField(default=None)
    updated = serializers.DateTimeField(default=None)
    deleted = serializers.DateTimeField(default=None)
    verified = serializers.DateTimeField(default=None)
    source_id = serializers.UUIDField(default=None)
    start_index = serializers.IntegerField(required=True)
    claim_type = serializers.IntegerField(required=True)

    def create(self, validated_data):
        claim = Claim.objects.create(**validated_data)
        claim.save()
        return claim

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.start_index = validated_data.get('start_index', instance.start_index)
        instance.source_id = validated_data.get('source_id', instance.source_id)
        instance.verified = validated_data.get('verified', instance.verified)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.updated = datetime.now()
        instance.save()
        return instance


class SourceSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=None)
    url = serializers.URLField(default=None)
    name = serializers.CharField(max_length = 255, required=True)
    description = serializers.CharField(default=None)
    created = serializers.DateTimeField(default=None)
    updated = serializers.DateTimeField(default=None)
    deleted = serializers.DateTimeField(default=None)
    source_type = serializers.IntegerField(default=None)

    def create(self, validated_data):
        source = Source.objects.create(**validated_data)
        source.save()
        return source

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.verified = validated_data.get('verified', instance.verified)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.updated = datetime.now()
        instance.save()
        return instance