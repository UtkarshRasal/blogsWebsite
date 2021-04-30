import csv
import json
import logging
from datetime import datetime

import pandas as pd
from base.pagination import SmallResultsSetPagination
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.viewsets import ModelViewSet, ViewSet

from blogs import mixins

from .utils import file_path
from .models import Activity, Blogs
from .serializers import CommentsSerializer, DateWiseSerializer


class BaseViewSet(ModelViewSet):
    '''viewset to perform crud operations'''

    pagination_class   = SmallResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    logging.basicConfig(filename='example.log', filemode='a', level=logging.INFO)

    '''fetch queryset'''
    def get_queryset(self):
        return self.model_class.objects.all()

    @method_decorator(cache_page(60*15))
    def list(self, request):
        assert self.serializer_class is not None
        assert self.model_class is not None
        
        #query param, if data between two dates is required
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        month  = request.GET.get('month')

        #if start_date and end_date is provided 
        if start_date and end_date is not None:
            try:
                instance = self.model_class.objects.filter(Q(created_at__gte = start_date)&Q(created_at__lte = end_date), user=request.user.pk)

                '''pagination'''
                page = self.paginate_queryset(instance)
                serializers = self.get_paginated_response(DateWiseSerializer(page, many=True).data)
                
                '''logging'''
                logging.info(f"{self.instance_name}'s from the dates {start_date} to {end_date} retrieved for the user'{request.user.pk}'") 

                return Response({   
                    'status':True,
                    'message':f'Blogs from the dates {start_date} to {end_date} retrieved successfully',
                    'data':serializers.data
                }, status=status.HTTP_200_OK)
            except:
                raise ValidationError(f'Date has an invalid format. It must be in YYYY-MM-DD')
        
        # if data for a particular month is required
        elif month is not None:
            try:
                instance = self.model_class.objects.filter(created_at__month__gte = month, user=request.user.pk)

                # pagination
                page = self.paginate_queryset(instance)
                serializers = self.get_paginated_response(DateWiseSerializer(page, many=True).data)

                # logging
                logging.info(f"{self.instance_name}'s of the month {month} retrieved for the user '{request.user.pk}'")
        
                return Response({   
                    'status':True,
                    'message':f'Blogs for the month {month} retrieved successfully',
                    'data':serializers.data
                }, status=status.HTTP_200_OK)
            except:
                raise ValidationError(f'Month has to be an integer value')

        # return all the blogs for a user
        else:
            instance = self.model_class.objects.filter(user=request.user.pk)
            # search filter
            queryset_list = self.filter_queryset(instance)

            # pagination
            page = self.paginate_queryset(queryset_list)
            serializers = self.get_paginated_response(self.serializer_class(page, many=True).data)

            # logging
            logging.info(f"{self.instance_name}'s listed for the user '{request.user.pk}'")  

            return Response({   
                'status':True,
                'message':f'{self.instance_name} retrieved successfully',
                'data':serializers.data
            }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        current_site = get_current_site(request).domain

        path = 'http://' + current_site + '/'
        if request.FILES.get('file'):
            path += file_path(request) # get path of the media_file

        tags = request.data['tags']

        if type(tags) is str:
            _tags = json.loads(tags) # convert string to dictionary

        else:
            _tags = tags
        
        tags = []

        # convert uppercase tags to lowercase
        for i in range(len(_tags)):
            tags.append({k: v.lower() for k, v in _tags[i].items()})


        serializers = self.get_serializer(data={**{'user':request.user.pk,
                                                    'media_file':path,
                                                    'title':request.data['title'],
                                                    'content':request.data['content'],
                                                    'tags':tags,
                                                    }})
        if serializers.is_valid():
            serializers.save()
            data = serializers.data
            
            # logging
            logging.info("created %s with title '%s'", self.instance_name, data['title'])
            blog = self.model_class.objects.get(id = data['id'])
            Activity.objects.create(user=request.user, blog=blog, logs = 'Blogs created Successfully')
            
            return Response(data={
                'status':True,
                'message':f"{self.instance_name} created Successfully",
                'data':serializers.data

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
        serializers = self.serializer_class(instance=instance)
        
        #logging
        logging.info(f"Retrieved {self.instance_name} '{serializers.data['id']}'")

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} retrived successfully',
            'data':serializers.data
        })
    
    def update(self, request, pk, *args, **kwargs):
        assert self.serializer_class is not None
        assert self.model_class is not None

        current_site = get_current_site(request).domain
        path = 'http://' + current_site + '/' + file_path(request)
        _tags = request.data['tags']
        
        if type(_tags) is str:
            tags = json.loads(_tags) # convert string to dictionary

        else:
            tags = _tags
        
        instance = self.model_class.objects.get(id=pk)
        serializers = self.get_serializer(instance=instance, data={**{'user':request.user.pk,
                                                    'media_file':path,
                                                    'title':request.data['title'],
                                                    'content':request.data['content'],
                                                    'tags':tags,
                                                    }})
        if serializers.is_valid():
            serializers.save()
            
            #logging
            logging.info("Updated %s '%s'", self.instance_name, pk)
            Activity.objects.create(user=request.user, blog=instance, logs = 'Blog updated Successfully')

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

    def partial_update(self, request, pk, *args, **kwargs):
        assert self.serializer_class is not None
        assert self.model_class is not None
        instance = self.model_class.objects.get(id=pk)
        
        '''check which data has to be updated'''
        if request.data.get('file'):
            current_site = get_current_site(request).domain
            path = 'http://' + current_site + '/' + file_path(request)
            _data = {'media_file':path}
        
        if request.data.get('title'):
            _data = {'title':request.data['title']}
        
        if request.data.get('content'):
            _data = {'content':request.data['content']}
        
        if request.data.get('tags'):
            _tags = json.loads(request.data['tags']) #convert string to dictionary  
            tags = []
            for i in range(len(_tags)):
                tags.append({k: v.lower() for k, v in _tags[i].items()})
            
            _data = {'tags':tags}

        serializers = self.get_serializer(instance=instance, data=_data, partial=True)
        if serializers.is_valid():
            serializers.save()

            #logging
            logging.info("Partially updated %s '%s'", self.instance_name, pk)
            Activity.objects.create(user=request.user, blog=instance, logs = 'Blog partially updated Successfully')

            return Response(data={
                'status':True,
                'message':f'{self.instance_name} updated Successfully',
                'data':serializers.data
            }, status=status.HTTP_201_CREATED)

        return Response(data={
                'status':False,
                'message':f'{self.instance_name} update Failed',
                'data':serializers.errors
            }, status=status.HTTP_400_BAD_REQUEST) 

    def destroy(self, request, pk, *args, **kwargs):
        assert self.model_class is not None
        instance = self.model_class.objects.filter(id=pk)
        instance.delete()

        #logging
        logging.info(f"Deleted {self.instance_name} '{pk}'")
        #   Activity.objects.create(user=request.user, blog=instance, logs = 'Blog deleted Successfully')

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} deleted',
        }, status=status.HTTP_200_OK)

class TagsViewSet(ModelViewSet):
    '''viewset to handle tags crud operation'''

    pagination_class = SmallResultsSetPagination
    def get_queryset(self):
        return self.model_class.objects.all()
    
    #list all the tags present
    def list(self, request, *args, **kwargs):
        queryset = self.model_class.objects.all()
        
        '''pagination'''
        page = self.paginate_queryset(queryset)
        serializers = self.get_paginated_response(self.serializer_class(page, many=True).data)

        '''logging'''
        logging.info("%s's listed for the user '%s'", self.instance_name, request.user.pk)
       
        return Response(data={
            'status':True,
            'message':f'{self.instance_name} listed successfully',
            'data':serializers.data
        })
