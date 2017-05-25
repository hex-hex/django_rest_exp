from django.shortcuts import render
from .models import Post
#.models means in the current folder

def post_list(request):
    '''Show the list of the blog
    and it is the first view
    '''
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request):
    post = Post.objects.get()
    return render(request, 'blog/post_detail.html',{'post':post})