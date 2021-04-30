from accounts.models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from blogs import mixins

from .models import Blogs, Tags
from .serializers import (ActivitySerializer, BlogCSVSerializer,
                          BlogLikesSerializer, BlogsLikeCommentSerializer,
                          BlogsSerializer, CommentCSVSerializer,
                          CommentsSerializer, LikeCSVSerializer,
                          TagsBlogSerializers, TagsSerializer,
                          TagsShowSerializer)
from .viewsets import BaseViewSet, TagsViewSet

class BlogsView(BaseViewSet, mixins.LikesMixin, mixins.CommentsMixin, mixins.ActivityMixin, mixins.LeaderBoardMixin):
    serializer_class    = BlogsSerializer
    model_class         = Blogs
    instance_name       = 'Blog'

    ACTION_SERIALIZERS  = {
        'post_comment': CommentsSerializer,
        'comment':CommentsSerializer,
        'likes':BlogLikesSerializer,
        'actvity':ActivitySerializer,
        'leaderboard':BlogsLikeCommentSerializer,
        'blogs_report':BlogCSVSerializer,
        'comment_report':CommentCSVSerializer,
        'likes_report': LikeCSVSerializer,
    }

    def get_serializer_class(self):
        return self.ACTION_SERIALIZERS.get(self.action, self.serializer_class)

class TagsView(TagsViewSet, mixins.TagsMixin):
    serializer_class     = TagsSerializer
    model_class          = Tags
    instance_name        = 'Tags'
    
    ACTION_SERIALIZERS   = {
        'blogs':TagsShowSerializer,
        'leaderboard':TagsBlogSerializers
    } 

    def get_serializer_class(self):
        return self.ACTION_SERIALIZERS.get(self.action, self.serializer_class)
