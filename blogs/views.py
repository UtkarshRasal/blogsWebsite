from blogs.models import Blogs, Comments
from blogs.serializers import BlogsSerializer, CommentsSerializer
from blogs.viewsets import BaseViewSet
from blogs import mixins

class BlogsView(BaseViewSet, mixins.LikesMixin, mixins.CommentsMixin):
    serializer_class = BlogsSerializer
    model_class      = Blogs
    instance_name    = 'Blog'

    def get_serializer_class(self):
        if self.action == 'post_comment':
            return CommentsSerializer
        if self.action == 'comment':
            return CommentsSerializer
        return BlogsSerializer
        
