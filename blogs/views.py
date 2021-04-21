from django.contrib.sites.shortcuts import get_current_site
from rest_framework.viewsets import ViewSet
from .models import Blogs, Comments, Tags, Activity
from .serializers import BlogsSerializer, CommentsSerializer, TagsShowSerializer, ActivitySerializer
from .viewsets import BaseViewSet, TagsViewSet
from .path import file_path
from blogs import mixins

class BlogsView(BaseViewSet, mixins.LikesMixin, mixins.CommentsMixin, mixins.ActivityMixin):
    serializer_class = BlogsSerializer
    model_class      = Blogs
    instance_name    = 'Blog'
    
    def get_serializer_class(self):
        if self.action == 'post_comment':
            return CommentsSerializer
        if self.action == 'comment':
            return CommentsSerializer
        if self.action == 'activity':
            return ActivitySerializer
        return BlogsSerializer

class TagsView(TagsViewSet, mixins.TagsMixin):
    serializer_class = TagsShowSerializer
    model_class      = Tags
    instance_name    = 'Tags'
