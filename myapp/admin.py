from django.contrib import admin
from .models import Post
#from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Post)
# Register your models here.

#TokenAdmin.raw_id_fields = ('user',)
