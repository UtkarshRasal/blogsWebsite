from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from base.pagination import SmallResultsSetPagination
from base import mixins
from .models import Blogs
from .path import file_path
import json

class BaseViewSet(ModelViewSet, mixins.PaginationHandlerMixin, mixins.BaseFilterMixin):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    '''fetch queryset'''
    def get_queryset(self):
        return self.model_class.objects.all()
    
    # def get_serializer_class(self):
    #     return self.serializer_class

    def list(self, request):
        assert self.serializer_class is not None
        assert self.model_class is not None
        instance = self.model_class.objects.filter(user=request.user.pk)

        '''search filter'''
        queryset_list = self.filter_queryset(instance)

        '''pagination'''
        page = self.paginate_queryset(queryset_list)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.get_serializer(instance, many=True)  

        return Response({   
            'status':True,
            'message':f'{self.instance_name} retrieved successfully',
            'data':serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        path = file_path(request) #get the path of the media file
        _tags = request.data['tags']
        tags = json.loads(_tags) #convert string to dictionary

        serializers = self.get_serializer(data={**{'user':request.user.pk,
                                                    'media_file':path,
                                                    'title':request.data['title'],
                                                    'content':request.data['content'],
                                                    'tags':tags,
                                                    }})
        if serializers.is_valid():
            serializers.save()
            data = serializers.data 
            current_site = get_current_site(request).domain
            absurl = 'http://' + current_site + '/' + file_path(request)
            data['media_file'] = absurl

            return Response(data={
                'status':True,
                'message':f"{self.instance_name} created Successfully",
                'data':data

            }, status=status.HTTP_201_CREATED)

        return Response(data={
            'status':False,
            'message':f"{self.instance_name} failed",
            'data':serializers.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        assert self.serializer_class is not None
        assert self.model_class is not None
        instance = self.model_class.objects.get(id=pk)
        serializer = self.serializer_class(instance=instance)

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} retrived successfully',
            'data':serializer.data
        })

    def partial_update(self, request, pk=None, *args, **kwargs):
        assert self.serializer_class is not None
        assert self.model_class is not None
        instance = self.model_class.objects.get(id=pk)
        serializers = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()

            return Response(data={
                'status':True,
                'message':f'{self.instance_name} updated Successfully',
                'data':serializers.data
            })

        return Response(data={
                'status':False,
                'message':f'{self.instance_name} update Failed',
                'data':serializers.errors
            }) 

    def destroy(self, request, pk, *args, **kwargs):
        assert self.model_class is not None
        instance = self.model_class.objects.filter(id=pk)
        instance.delete()

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} deleted',
        }, status=status.HTTP_200_OK)