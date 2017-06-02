from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers
from myapp.models import Post
import time


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')

    def create(self, validated_data):
        # This is a very inevitable override
        post = Post(
            title=validated_data['title'],
            text=validated_data['text'],
            author=validated_data['owner']
        )
        post.published_date = timezone.now()
        post.save()
        # remember this function
        return post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = False
        if password is not None:
            instance.set_password(password)
        instance.save()
        print(instance.password)
        return instance

