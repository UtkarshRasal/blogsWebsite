from blogs.models import Blogs, Comments, Likes
from blogs.serializers import BlogsSerializer, CommentsSerializer, LikesSerializer
from blogs.viewsets import BaseViewSet

class BlogsView(BaseViewSet):
    serializer_class = BlogsSerializer
    model_class      = Blogs
    instance_name    = 'Blog'

class CommentsView(BaseViewSet):
    serializer_class = CommentsSerializer
    model_class      = Comments
    instance_name    = 'Comment'

class LikesView(BaseViewSet):
    serializer_class = LikesSerializer
    model_class      = Likes
    instance_name    = 'Like'
