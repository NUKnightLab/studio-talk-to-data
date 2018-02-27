from django.contrib.auth.models import User, Group
from rest_framework import serializers
from datetime import datetime


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
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'username')
        write_only_fields = ('password')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
