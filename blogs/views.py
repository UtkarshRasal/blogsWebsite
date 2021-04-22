from django.contrib.sites.shortcuts import get_current_site
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blogs, Comments, Tags, Activity, LeaderBoard
from .serializers import ( BlogsSerializer, CommentsSerializer, 
                           TagsShowSerializer, ActivitySerializer, 
                           BlogsCommentSerializer)
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
            return BlogsCommentSerializer
        return BlogsSerializer

class TagsView(TagsViewSet, mixins.TagsMixin):
    serializer_class = TagsShowSerializer
    model_class      = Tags
    instance_name    = 'Tags'

class UserView(APIView):
    serializer_class = BlogsCommentSerializer
    model_class = Blogs

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        serializer = self.serializer_class(self.model_class.objects.all(), many=True)

        return Response(sorted(serializer.data, key=lambda blog: blog['comments_count'], reverse=True))
