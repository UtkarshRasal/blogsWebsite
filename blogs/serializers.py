from rest_framework import serializers
from .models import Blogs, Comments, Tags, Activity, LeaderBoard
from accounts.serializers import UserShowSerializer
from accounts.models import User


class TagsShowSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()


    class Meta:
        model  = Blogs
        fields = ['id','count', 'title', 'tags']
        depth = 1
    
    def get_count(self, obj):
        return obj.tags.count()

    
class BlogsActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model  = Blogs
        fields = ['id', 'title']

class TagsBlogSerializers(serializers.ModelSerializer):
    blogs = BlogsActivitySerializer(many=True)
    blogs_count = serializers.SerializerMethodField()

    class Meta:
        model  = Tags       
        fields = ['name', 'blogs_count', 'blogs']
    
    def get_blogs_count(self, obj):
        return obj.blogs.count()
        
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']


class BlogsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(required=False, many=True)

    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'tags', 'media_file', 'created_at', 'updated_at']

    
    ''' tags create and update'''
    def create(self, validated_data):
        _tags = validated_data.pop("tags", [])
        tag_list = []
        for tag in _tags:
            _tag, _ = Tags.objects.get_or_create(**tag)
            tag_list.append(_tag.pk)

        _blog = Blogs.objects.create(**validated_data)

        _blog.tags.set(tag_list)

        return _blog

    def update(self, instance, validated_data):
        _tags = validated_data.pop("tags", [])
        tag_list = []
        for tag in _tags:
            _tag, _ = Tags.objects.get_or_create(**tag)
            tag_list.append(_tag.pk)
        instance.tags.clear()
        instance.tags.set(tag_list)

        return super(BlogsSerializer,
                     self).update(instance, validated_data)
                
class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Comments
        fields = '__all__'

class BlogLikesSerializer(serializers.ModelSerializer):
    likes = UserShowSerializer(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model  = Blogs
        fields = ['likes_count', 'likes']
    
    def get_likes_count(self, obj):
        return obj.likes.count()

class ActivitySerializer(serializers.ModelSerializer):
    # blog = BlogsActivitySerializer()
    # user = UserShowSerializer()

    class Meta:
        model  = Activity
        fields = '__all__'
        depth  = 2

class UserBlogSerializer(serializers.ModelSerializer):
    user_blogs = BlogsSerializer(many=True)
    likes      = BlogsSerializer(many=True) 

    class Meta:
        model  = User
        fields = '__all__'

class BlogsLikeCommentSerializer(serializers.ModelSerializer):
    likes_count   =  serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField() 

    class Meta:
        model  = Blogs
        fields = ['id','title', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()