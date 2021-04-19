from rest_framework import pagination, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from blogs.models import Comments

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

            return Response(data={
                'status':True,
                'message':f"{self.instance_name} created Successfully",
                'data':serializers.data

            }, status=status.HTTP_201_CREATED)

        return Response(data={
            'status':False,
            'message':f"{self.instance_name} creation failed",
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
    
        return Response(data={
            'status':True,
            'message':f'Comments retrieved successfully',
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

            return Response(data={
                'status':True,
                'message':f'{self.instance_name} disliked successfully',
            })
        
        blogs.likes.add(_user)
        return Response(data={
            'status':True,
            'message':f'{self.instance_name} liked successfully',
        })

