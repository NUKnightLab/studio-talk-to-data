from django.db import models
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    text = models.TextField()

    class Meta:
        ordering = ('created',)

class Claim(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_id = models.UUIDField(default=None, null=True, editable=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    verified = models.DateTimeField(null=True)
    source_id = models.UUIDField(default=None, null=True, editable=True)
    start_index = models.IntegerField()
    claim_type = models.IntegerField()

    class Meta:
        ordering = ('article_id',)

class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    name = models.CharField(max_length = 255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    source_type = models.IntegerField()

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)

    class Meta:
        ordering = ('created',)
