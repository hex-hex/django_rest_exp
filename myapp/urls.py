from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

'''
there must be 'from .' or else it will search the module from root
'''

router = DefaultRouter()
router.register(r'Post', views.PostViewSet)

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^post/', include(router.urls)),

    url(r'^posts/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^posts/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^posts/new/$', views.post_new, name='post_new')
]