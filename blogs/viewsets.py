from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import permissions, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from base.pagination import SmallResultsSetPagination
from blogs import mixins
from .models import Blogs, Activity
from .serializers import DateWiseSerializer
from .path import file_path
import json, logging

class BaseViewSet(ModelViewSet):
    pagination_class   = SmallResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    logging.basicConfig(filename='example.log', filemode='a', level=logging.INFO)

    '''fetch queryset'''
    def get_queryset(self):
        return self.model_class.objects.all()
    
    def list(self, request):
        assert self.serializer_class is not None
        assert self.model_class is not None
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        month    = request.GET.get('month')

        if start_date and end_date is not None:
            try:
                instance = self.model_class.objects.filter(Q(created_at__gte = start_date)&Q(created_at__lte = end_date), user=request.user.pk)
                # '''search filter'''
                # queryset_list = super().filter_queryset(instance)

                '''pagination'''
                page = self.paginate_queryset(instance)
                if page is not None:
                    serializers = self.get_paginated_response(DateWiseSerializer(page, many=True).data)

                    #logging
                    logging.info("%s's listed for the user '%s'", self.instance_name, request.user.pk)
                else:
                    serializers = self.get_serializer(instance, many=True)  

                return Response({   
                    'status':True,
                    'message':f'Blogs from the dates {start_date} to {end_date} retrieved successfully',
                    'data':serializers.data
                }, status=status.HTTP_200_OK)
            except:
                raise ValidationError(f'Date has an invalid format. It must be in YYYY-MM-DD')
            
        elif month is not None:
            try:
                instance = self.model_class.objects.filter(created_at__month__gte = month, user=request.user.pk)
                # '''search filter'''
                # queryset_list = super().filter_queryset(instance)

                '''pagination'''
                page = self.paginate_queryset(instance)
                if page is not None:
                    serializers = self.get_paginated_response(DateWiseSerializer(page, many=True).data)

                    #logging
                    logging.info("%s's listed for the user '%s'", self.instance_name, request.user.pk)
                else:
                    serializers = self.get_serializer(instance, many=True)  

                return Response({   
                    'status':True,
                    'message':f'Blogs for the month {month} retrieved successfully',
                    'data':serializers.data
                }, status=status.HTTP_200_OK)
            except:
                raise ValidationError(f'Month has to be in integer value')


        else:
            instance = self.model_class.objects.filter(user=request.user.pk)
            '''search filter'''
            queryset_list = super().filter_queryset(instance)

            '''pagination'''
            page = self.paginate_queryset(queryset_list)
            if page is not None:
                serializers = self.get_paginated_response(self.serializer_class(page, many=True).data)

                #logging
                logging.info("%s's listed for the user '%s'", self.instance_name, request.user.pk)
            else:
                serializers = self.get_serializer(instance, many=True)  

            return Response({   
                'status':True,
                'message':f'{self.instance_name} retrieved successfully',
                'data':serializers.data
            }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        current_site = get_current_site(request).domain
        path = 'http://' + current_site + '/' + file_path(request)

        _tags = json.loads(request.data['tags']) #convert string to dictionary  
        tags = []
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

            logging.info("created %s with title '%s'", self.instance_name, data['title'])
            blog = self.model_class.objects.get(id=data['id'])
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
        logging.info("Retrieved %s '%s'", self.instance_name, serializers.data['id'])

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
        tags = json.loads(_tags)
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

        if request.data.get('file'):
            current_site = get_current_site(request).domain
            path = 'http://' + current_site + '/' + file_path(request)
            data = {'media_file':path}
        
        if request.data.get('title'):
            data = {'title':request.data['title']}
        
        if request.data.get('content'):
            data = {'content':request.data['content']}
        
        if request.data.get('tags'):
            _tags = json.loads(request.data['tags']) #convert string to dictionary  
            tags = []
            for i in range(len(_tags)):
                tags.append({k: v.lower() for k, v in _tags[i].items()})
            
            data = {'tags':tags}

        serializers = self.get_serializer(instance=instance, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()

            logging.info("Partially updated %s '%s'", self.instance_name, pk)
            Activity.objects.create(user=request.user, blog=instance, logs = 'Blog partially updated Successfully')

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

        #logging
        logging.info("Deleted %s '%s'", self.instance_name, pk)
        Activity.objects.create(user=request.user, blog=instance, logs = 'Blog deleted Successfully')

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} deleted',
        }, status=status.HTTP_200_OK)

class TagsViewSet(ModelViewSet):
    pagination_class = SmallResultsSetPagination
    def get_queryset(self):
        return self.model_class.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.model_class.objects.all()
        # serializers = self.serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializers = self.get_paginated_response(self.serializer_class(page, many=True).data)

            #logging
            logging.info("%s's listed for the user '%s'", self.instance_name, request.user.pk)
        else:
            serializers = self.get_serializer(instance, many=True)

        return Response(data={
            'status':True,
            'message':f'{self.instance_name} listed successfully',
            'data':serializers.data
        })