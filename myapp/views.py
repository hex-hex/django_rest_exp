from django.shortcuts import render

def post_list(request):
    '''Show the list of the blog
    and it is the first view
    '''
    return render(request, 'blog/post_list.html', {})
