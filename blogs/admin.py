from django.contrib import admin
from .models import Blogs, Comments, Tags, Activity, LeaderBoard

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(Tags)
admin.site.register(Activity)
admin.site.register(LeaderBoard)