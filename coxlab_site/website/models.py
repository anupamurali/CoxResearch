import datetime

from django.db import models
from djangotoolbox.fields import ListField

from django.utils import timezone
from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.fields import GridFSField

import os
from django import forms

from .forms import ObjectListField, StringListField
from django_mongodb_engine.storage import GridFSStorage
gridfs_storage = GridFSStorage()

#from gridfsuploads import gridfs_storage



class EmbedOverrideField(EmbeddedModelField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, ObjectListField, **kwargs)

class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)

class Video(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=255)
    caption = models.TextField(null=True)
    video = models.FileField(storage=gridfs_storage, upload_to='/')
    tags = CategoryField()
    comments = CategoryField(EmbedOverrideField('Comment'), blank=True)
    
    def __str__():
        return self.title

class Comment(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    author = EmbedOverrideField('Author')
    comment_text = models.TextField()

    def __str__():
        return self.comment_text

class  Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.email)
        
class User(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    """
    HAVE SOME MORE FIELDS FOR USER
    """
    videos = CategoryField(EmbedOverrideField('Video'))

# class Post(models.Model):
#     pub_date = models.DateTimeField(auto_now_add=True, null=True) # <---
#     title = models.CharField(max_length=255)
#     post_text = models.TextField()
#     tags = CategoryField()
#     comments = CategoryField(EmbedOverrideField('Comment'))

#     def __str__(self):
#         return self.post_text

#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now

#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'

# class Comment(models.Model):
#     created_on = models.DateTimeField(auto_now_add=True, null=True)
#     author = EmbedOverrideField('Author')
#     comment_text = models.TextField()

#     def __str__(self):
#         return self.comment_text

# class Author(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()

#     def __unicode__(self):
#         return '%s (%s)' % (self.name, self.email)

