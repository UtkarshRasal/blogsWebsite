from django.contrib.sites.shortcuts import get_current_site
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blogs, Comments, Tags, Activity, LeaderBoard
from .serializers import ( BlogsSerializer, CommentsSerializer, 
                           TagsShowSerializer, ActivitySerializer, 
                           BlogsLikeCommentSerializer)
from .viewsets import BaseViewSet, TagsViewSet
from .path import file_path
from blogs import mixins
from accounts.models import User

class BlogsView(BaseViewSet, mixins.LikesMixin, mixins.CommentsMixin, mixins.ActivityMixin, mixins.LeaderBoardMixin):
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
        if self.action == 'leaderboard':
            return BlogsLikeCommentSerializer
        return BlogsSerializer

class TagsView(TagsViewSet, mixins.TagsMixin):
    serializer_class = TagsShowSerializer
    model_class      = Tags
    instance_name    = 'Tags'
