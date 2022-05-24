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
      
      
      MODELS

from django.db import models
import uuid

class DataModel(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, unique=True)
    date = models.DateField()
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=50)
    approved_by = models.CharField(max_length=50)
    file = models.FileField(upload_to='')
    file_path = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    report_number = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count']
        verbose_name_plural = 'DataModel'

    def __str__(self) -> str:
        return f'{self.title}-{self.authors}-{self.date}'

class TechnicalMemoModel(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, unique=True)
    date = models.DateField()
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=50)
    file = models.FileField(upload_to='')
    file_path = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    report_number = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count']
        verbose_name_plural = 'TechnicalMemoModel'

    def __str__(self) -> str:
        return f'{self.title}-{self.authors}-{self.date}'

class ECReportModel(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, unique=True)
    date = models.DateField()
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=50)
    file = models.FileField(upload_to='')
    file_path = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    report_number = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count']
        verbose_name_plural = 'ECReportModel'

    def __str__(self) -> str:
        return f'{self.title}-{self.authors}-{self.date}'

SERIALIZERS

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import DataModel, TechnicalMemoModel, ECReportModel

class DataSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    image_path = serializers.CharField(required=False)
    class Meta:
        model = DataModel
        fields = '__all__'

class TechnicalMemoSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    image_path = serializers.CharField(required=False)
    class Meta:
        model = TechnicalMemoModel
        fields = '__all__'

class ECReportSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    image_path = serializers.CharField(required=False)
    class Meta:
        model = ECReportModel
        fields = '__all__'

class FileContentSerializer(ModelSerializer):

    class Meta: 
        model = DataModel
        fields = ['title', 'file']

class DisplayDataSerializer(ModelSerializer):

    class Meta:
        model = DataModel
        fields = ['id', 'date', 'title', 'authors', 'approved_by', 'file', 
                    'file_path', 'image', 'image_path', 'report_number', 'count']

VIEWS

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from docxtpl import DocxTemplate

from .models import DataModel, TechnicalMemoModel, ECReportModel
from .serializers import (DataSerializer, DisplayDataSerializer,
                          TechnicalMemoSerializer, ECReportSerializer )
from .utils import get_serial_number
from .sharepoint import Sharepoint


import os

class UploadData(APIView):
    def get(self, request):
        return render(request, 'upload.html')

class TechnicalReport(APIView):
    serializer_class = DataSerializer
    model_class = DataModel

    def post(self, request):
        data = request.data
        for field in ['date', 'title', 'authors', 'approved_by']:
            if not data.get(field):
                return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)

        current_site = get_current_site(request).domain
        # _file_path = f"http://{current_site}/downloaded_file/{request.FILES['file'].name}"
        _file_path = os.path.join(settings.BASE_DIR, f"downloaded_file\{request.FILES['file'].name}")

        file = request.FILES['file']
        file_name = request.FILES['file'].name.split('.')

        # Check if the file is in document format, if not return error
        if(file_name[1] != 'docx' and file_name[1] != 'doc'):
            
            return Response({
                'status': False,
                'message': 'File is not a word document'
            })

        # report_number generation
        serial_num, count = get_serial_number(data['techreport'])
        report_number = f"{data['date'].split('-')[0]}TR{serial_num}"

        data_dict = {
            'date': data['date'],
            'title': data['title'].capitalize(),
            'authors': data['authors'].capitalize(),
            'approved_by': data['approved_by'].capitalize(),
            'file': request.FILES['file'],
            'file_path': _file_path,
            'report_number':report_number,
            'count': (count+1)
        }

        if request.FILES.get('image', False):
            data_dict['image'] = request.FILES['image']
            data_dict['image_path'] = (f"http://{current_site}/downloaded_file/{request.FILES['image'].name}") if request.FILES.get('image', False) else ""

        serializer = self.serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.data 

        # # Upload to sharepoint folder
        # new_file_name = serializer.data['file'].split('/')[2]
        # file_dir = os.path.join(settings.BASE_DIR, f"downloaded_file\\{new_file_name}")
        # folder_name = 'Technical Report'

        # Sharepoint().upload_to_sharepoint(file_dir, new_file_name, folder_name)

        return render(request, 'upload.html', {'report_data': serializer.data})
        
        # return Response({
        #     'status': True,
        #     'message': f"Data uploaded and Report number generated is-{data['report_number']}",
        #     'data': data
        # })

class TechnicalMemo(APIView):
    serializer_class = TechnicalMemoSerializer
    model_class = TechnicalMemoModel

    def post(self, request):
        data = request.data
        for field in ['date', 'title', 'authors']:
            if not data.get(field):
                return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)

        current_site = get_current_site(request).domain
        # _file_path = f"http://{current_site}/downloaded_file/{request.FILES['file'].name}"
        _file_path = os.path.join(settings.BASE_DIR, f"downloaded_file\{request.FILES['file'].name}")

        file = request.FILES['file']
        file_name = request.FILES['file'].name.split('.')

        # Check if the file is in document format, if not return error
        if(file_name[1] != 'docx' and file_name[1] != 'doc'):
            
            return Response({
                'status': False,
                'message': 'File is not a word document'
            })

        # report_number generation
        serial_num, count = get_serial_number(data['techmemo'])
        report_number = f"{data['date'].split('-')[0]}TM{serial_num}"

        data_dict = {
            'date': data['date'],
            'title': data['title'].capitalize(),
            'authors': data['authors'].capitalize(),
            'file': request.FILES['file'],
            'file_path': _file_path,
            'report_number':report_number,
            'count': (count+1)
        }

        if request.FILES.get('image', False):
            data_dict['image'] = request.FILES['image']
            data_dict['image_path'] = (f"http://{current_site}/downloaded_file/{request.FILES['image'].name}") if request.FILES.get('image', False) else ""

        serializer = self.serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.data 

        # # Upload to sharepoint folder
        # new_file_name = serializer.data['file'].split('/')[2]
        # file_dir = os.path.join(settings.BASE_DIR, f"downloaded_file\\{new_file_name}")
        # folder_name = 'Technical Report'

        # Sharepoint().upload_to_sharepoint(file_dir, new_file_name, folder_name)

        return render(request, 'upload.html', {'memo_data': serializer.data})
        
        # return Response({
        #     'status': True,
        #     'message': f"Data uploaded and Report number generated is-{data['report_number']}",
        #     'data': data
        # })

class ECReport(APIView):
    serializer_class = ECReportSerializer
    model_class = ECReportModel

    def post(self, request):
        data = request.data
        for field in ['date', 'title', 'authors', 'approved_by']:
            if not data.get(field):
                return Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)

        current_site = get_current_site(request).domain
        # _file_path = f"http://{current_site}/downloaded_file/{request.FILES['file'].name}"
        _file_path = os.path.join(settings.BASE_DIR, f"downloaded_file\{request.FILES['file'].name}")

        file = request.FILES['file']
        file_name = request.FILES['file'].name.split('.')

        # Check if the file is in document format, if not return error
        if(file_name[1] != 'docx' and file_name[1] != 'doc'):
            
            return Response({
                'status': False,
                'message': 'File is not a word document'
            })

        # report_number generation
        serial_num, count = get_serial_number(data['ecreport'])
        report_number = f"{data['date'].split('-')[0]}ECR{serial_num}"

        data_dict = {
            'date': data['date'],
            'title': data['title'].capitalize(),
            'authors': data['authors'].capitalize(),
            'approved_by': data['approved_by'].capitalize(),
            'file': request.FILES['file'],
            'file_path': _file_path,
            'report_number':report_number,
            'count': (count+1)
        }

        if request.FILES.get('image', False):
            data_dict['image'] = request.FILES['image']
            data_dict['image_path'] = (f"http://{current_site}/downloaded_file/{request.FILES['image'].name}") if request.FILES.get('image', False) else ""

        serializer = self.serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.data 

        # # Upload to sharepoint folder
        # new_file_name = serializer.data['file'].split('/')[2]
        # file_dir = os.path.join(settings.BASE_DIR, f"downloaded_file\\{new_file_name}")
        # folder_name = 'Technical Report'

        # Sharepoint().upload_to_sharepoint(file_dir, new_file_name, folder_name)

        return render(request, 'upload.html', {'ecr_data': serializer.data})
        
        # return Response({
        #     'status': True,
        #     'message': f"Data uploaded and Report number generated is-{data['report_number']}",
        #     'data': data
        # })

class FileContent(APIView):
    model_class = DataModel
    serializer_class = DataSerializer

    def get(self, request, *args, **kwargs):
        instance = self.model_class.objects.get(id=kwargs.get('pk'))
        serializer = self.serializer_class(instance=instance)
        
        # edit report template
        doc = DocxTemplate(serializer.data['file_path'])
        context = {
            'title': serializer.data['title'],
            'date': serializer.data['date'],
            'author': serializer.data['authors'],
            'approved_by': serializer.data['approved_by'],
            }
        
        doc.render(context)

        if(os.path.exists('.\\edited_documents\\') != True):
            os.mkdir('.\edited_documents')

        new_file = os.path.join(settings.BASE_DIR, f"edited_documents\{serializer.data['report_number']}.docx")
        doc.save(new_file)

        # Upload to sharepoint folder
        file_name = f"{serializer.data['report_number']}.docx"
        file_dir = new_file
        folder_name = 'Technical Report'

        Sharepoint().upload_to_sharepoint(file_dir, file_name, folder_name)


        return Response({
            'status': True,
            'message': 'Data fetched successfully',
            'data': serializer.data
        })


class DisplayData(APIView):
    model_class = DataModel
    serializer_class = DisplayDataSerializer

    def get(self, request):
        queryset = self.model_class.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        
        if queryset:
            return Response({
                'status': True,
                'message': 'Display Data',
                'data':serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
                'status': False,
                'message': 'Queryset not found',
            }, status=status.HTTP_404_NOT_FOUND) 
 
UTILS

from .models import DataModel, TechnicalMemoModel, ECReportModel

def get_serial_number(report_type):
    if report_type == 'techreport': queryset = DataModel.objects.first()
    if report_type == 'techmemo': queryset = TechnicalMemoModel.objects.first()
    if report_type == 'ecreport': queryset = ECReportModel.objects.first() 

    if not queryset:
        count = 1
    else:
        count = queryset.count
    
    len_count = len(str(count))

    if len_count == 1:
        serial_num = '00' + str(count)
    elif len_count == 2:
        serial_num = '0' + str(count)
    else:
        serial_num = str(count)
    
    return serial_num, count

URLS

from email.policy import default
from os import stat
from xml.etree.ElementInclude import include
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fetchDocument import views

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('upload', views.UploadData.as_view(), name='uploadDocument'),
    path('techreport', views.TechnicalReport.as_view(), name='techreport'),
    path('techmemo', views.TechnicalMemo.as_view(), name='techmemo'),
    path('ecreport', views.ECReport.as_view(), name='ecreport'),
    path('filecontent/<str:pk>', views.FileContent.as_view(), name='filecontent'),
    path('displaydata', views.DisplayData.as_view(), name='displayData'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# router = DefaultRouter()
# router.register(r'techreport', views.TechnicalReportView, basename='technical_report')

# urlpatterns = [
#     path('', include(router.urls))
# ]


SHAREPOINT

from sqlite3 import connect
from shareplum import Site, Office365
from shareplum.site import Version

from dotenv import dotenv_values
from django.conf import settings

import json, os


config = dotenv_values('.env')

USERNAME = config['USER']
PASSWORD = config['PASSWORD']
SHAREPOINT_URL = config['URL']
SHAREPOINT_SITE = config['SITE'] 
SHAREPOINT_DOC = config['DOC_LIBRARY']

class Sharepoint:
    def auth(self):
        authcookie = Office365(SHAREPOINT_URL, username=USERNAME, password=PASSWORD).get_cookies()
        site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=authcookie)

        return site
    
    def connect_folder(self, folder_name):
        auth_site = self.auth()
        sharepoint_dir = '/'.join([SHAREPOINT_DOC, folder_name])
        folder = auth_site.Folder(sharepoint_dir)

        return folder
    
    def upload_to_sharepoint(self, file, file_name, folder_name):
        folder = self.connect_folder(folder_name)

        with open(file, 'rb') as fp:
            file_content = fp.read()
        
        folder.upload_file(file_content, file_name)

    def delete_from_sharepoint(self, file_name, folder_name):
        folder = self.connect_folder(folder_name)

        folder.delete_file(file_name)


SETTINGS

MEDIA_ROOT = os.path.join(BASE_DIR, 'downloaded_file')
MEDIA_URL = '/downloaded_file/'



