from rest_framework import pagination, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from blogs.models import Comments, Blogs, Activity, LeaderBoard
from accounts.models import User
from .serializers import (BlogLikesSerializer, BlogsSerializer, BlogsCommentSerializer, BlogLikeSerializer)
import logging

class BaseFilterMixin:
    search_fields = ['title', 'content']
    filter_backends = (SearchFilter, )

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

class CommentsMixin:
    permission_classes = [permissions.IsAuthenticated]
    @action(methods=['POST'], detail=True)
    def post_comment(self, request, pk, *args, **kwargs):
        user = request.data

        '''check if blog exist or not'''
        if not self.model_class.objects.filter(id=pk).exists():
            return Response(data={
                'status':False,
                'message':f'Blog not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        blog = self.model_class.objects.get(id=pk)
        serializers = self.get_serializer(data={**user, **{'user':request.user.pk,
                                                             'blog':blog.id}})
        if serializers.is_valid():
            serializers.save()

            logging.info("Commented on %s '%s'", self.instance_name, pk)
            Activity.objects.create(user=request.user, blog=blog, logs = f"Commented on the blog '{pk}'")
            return Response(data={
                'status':True,
                'message':f"comment created Successfully",
                'data':serializers.data

            }, status=status.HTTP_201_CREATED)

        return Response(data={
            'status':False,
            'message':f"comment creation failed",
            'data':serializers.errors

        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=True)
    def comment(self, request, pk,  *args, **kwargs):
        if not self.model_class.objects.filter(id=pk).exists():
            return Response(data={
                'status':False,
                'message':f'Blog not found'
            })
        
        blog = self.model_class.objects.get(id=pk)

        instance = Comments.objects.filter(blog=blog.id)
        serializer = self.get_serializer(instance=instance, many=True)

        #logging
        logging.info("Commented retrieved for %s '%s'", self.instance_name, pk)
        Activity.objects.create(user=request.user, blog=blog, logs = f"Commented retrieved for blog '{pk}'")
    
        return Response(data={
            'status':True,
            'message':f'Comments retrieved successfully',
            'data':serializer.data
        })
    @action(methods=['DELETE'], detail=True)
    def comment(self, request, pk, *args, **kwargs):
        assert self.model_class is not None
        instance = Comments.objects.get(id=pk)
        instance.delete()

        #logging
        logging.info("Deleted Comment '%s'", self.instance_name, pk)

        return Response(data={
            'status':True,
            'message':f'Comment deleted',
        }, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=True)
    def comments_count(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        blogs = self.model_class.objects.get(id=kwargs.get('pk'))
        serializer = BlogsCommentSerializer(instance=blogs)

        return Response(data={
            'status':True,
            'message': f"Total Likes of user {kwargs.get('pk')}",
            'data':serializer.data
        })


class LikesMixin:
    @action(methods=['POST'], detail=True)
    def like_dislike(self, request, *args, **kwargs):
        if not self.model_class.objects.filter(id=kwargs.get('pk')).exists():
            return Response(data={
                'status':False,
                'message':f'Blog not found'
            })
        blogs = self.model_class.objects.get(id=kwargs.get('pk'))
        
        _user = self.request.user.pk
        if blogs.likes.filter(id=_user).exists():
            blogs.likes.remove(_user)
            print("like", blogs.likes.count())

            logging.info("Disliked %s '%s'", self.instance_name, kwargs.get('pk'))
            Activity.objects.create(user=request.user, blog=blogs, logs = f"Disliked blog '{kwargs.get('pk')}'")

            return Response(data={
                'status':True,
                'message':f'{self.instance_name} disliked successfully',
            })
        
        blogs.likes.add(_user)
        print("comment", blogs.comments.count())

        logging.info("Liked %s '%s'", self.instance_name, kwargs.get('pk'))
        Activity.objects.create(user=request.user, blog=blogs, logs = f"Liked blog '{kwargs.get('pk')}'")

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} liked successfully',
        })

    @action(methods=['GET'], detail=True)
    def likes(self, request, *args, **kwargs):
        if not self.model_class.objects.filter(id=kwargs.get('pk')).exists():
            return Response(data={
                'status':False,
                'message':f'Blog not found'
            })
        blogs = self.model_class.objects.get(id=kwargs.get('pk'))
        serializer = BlogLikesSerializer(instance=blogs)

        return Response(data={
            'status':True,
            'message': f"Total Likes of user {kwargs.get('pk')}",
            'data':serializer.data
        })

class ActivityMixin:
    @action(methods=['GET'], detail=True)
    def activity(self, request, *args, **kwargs):
        if not self.model_class.objects.filter(id=kwargs.get('pk')).exists():
            return Response(data={
                'status':False,
                'message':f'Blog not found'
            })

        # user = User.get(id=kwargs.get('pk'))
        instance = Activity.objects.filter(user=request.user)
        serializers = self.get_serializer(instance=instance, many=True)

        return Response(data={
            'status':True,
            'message':f"All the activities of blog {kwargs.get('pk')}",
            'data':serializers.data
        })

class TagsMixin:
    @action(methods=['GET'], detail=False, url_path="(?P<name>[^/.]+)/blogs", url_name='blogs')
    def blogs(self, request,*args, **kwargs):
        tagname = kwargs.get('name')
        blogs = Blogs.objects.filter(tags__name = tagname)

        serializer = BlogsSerializer(blogs, many=True)

        return Response(data={
            'status':True,
            'message':f'this is the {tagname} of the tag',
            'data':serializer.data
        })

class LeaderBoardMixin: 

    @action(methods=['GET'], detail=False, url_path='leaderboard', url_name='leaderboard')
    def leaderboard(self, request, *args, **kwargs):
        query_param = request.GET.get('param')

        if query_param=='likes':        
            serializer = BlogLikeSerializer(self.model_class.objects.all(), many=True)

            return Response(sorted(serializer.data, key=lambda blog: blog['likes_count'], 
                                    reverse = True if query_param=='likes' else False))
        
        # if query_param=='comments':
        serializer = BlogLikeSerializer(self.model_class.objects.all(), many=True)

        return Response(sorted(serializer.data, key=lambda blog: blog['comments_count'], 
                                reverse = True if query_param=='comments' else False))
        