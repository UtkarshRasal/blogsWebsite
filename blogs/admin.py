from django.contrib import admin
from .models import Blogs, Comments, Likes, Tags

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Tags)