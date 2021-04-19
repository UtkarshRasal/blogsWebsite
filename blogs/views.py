from blogs.models import Blogs, Comments, Likes
from blogs.serializers import BlogsSerializer, CommentsSerializer, LikesSerializer
from blogs.viewsets import BaseViewSet
from blogs import mixins

class BlogsView(BaseViewSet, mixins.CommentsMixin):
    serializer_class = BlogsSerializer
    model_class      = Blogs
    instance_name    = 'Blog'

    def get_serializer_class(self):
        if self.action == 'create':
            return BlogsSerializer
        if self.action == 'post_comment':
            return CommentsSerializer
        if self.action == 'comment':
            return CommentsSerializer

class LikesView(BaseViewSet):
    serializer_class = LikesSerializer
    model_class      = Likes
    instance_name    = 'Like'
