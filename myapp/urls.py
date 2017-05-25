from django.conf.urls import url
from . import views
'''
there must be 'from .' or else it will search the module from root
'''

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
]