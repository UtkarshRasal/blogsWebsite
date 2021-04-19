from django.contrib import admin
from .models import Blogs, Comments, Tags

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(Tags)