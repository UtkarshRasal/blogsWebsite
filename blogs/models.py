from django.db import models
from accounts.models import User
from base.models import BaseModel
import datetime, uuid

class Tags(models.Model):
    ''' model for tags creation'''

    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True)
    name            = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
        
class Blogs(BaseModel):
    '''blogs model'''

    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title           = models.CharField(max_length=255)
    content         = models.TextField()
    tags            = models.ManyToManyField(Tags)
    likes           = models.ManyToManyField(User, related_name='likes')
    media_file      = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

class Comments(BaseModel):
    '''comments model with foreign keys to blog and users'''
 
    blog            = models.ForeignKey(Blogs, null=True, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment         = models.TextField()

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Comments'

    def __all__(self):
        return self.id 

class Activity(BaseModel):
    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    blog           = models.ForeignKey(Blogs, null=True, on_delete=models.CASCADE)

    logs            = models.CharField(max_length=255)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Activity'
    