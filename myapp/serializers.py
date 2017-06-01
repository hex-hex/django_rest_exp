from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'title', 'text')

