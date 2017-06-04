import jwt
from django.contrib.auth.models import User
from django.db.migrations import serializer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from requests import exceptions
from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler, jwt_decode_handler
from myapp.serializers import PostSerializer, UserSerializer
from .models import Post
from .form import PostForm


class ActivateUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        token = kwargs.pop('token')
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user_to_activate = User.objects.get(id=payload.get('user_id'))
        user_to_activate.is_active = True
        user_to_activate.save()

        return Response(
            {'User Activated'},
            status=status.HTTP_200_OK
        )


class CreateUserView(CreateAPIView):
    model = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.model.get(username=serializer.data['username'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response(
            {
                'confirmation_url': reverse(
                    'activate-user',
                    args=[token],
                    request=request
                )

            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def post_list(request):
    '''Show the list of the blog
    and it is the first view
    '''
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_new.html', {'form': form})