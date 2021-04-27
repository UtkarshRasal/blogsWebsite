from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid, datetime
from .userManager import UserManager

"""custom user model"""
class User(AbstractUser, models.Model):
	id			 = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
	username	 = None
	email		 = models.EmailField(max_length=255, unique=True, db_index=True)
	is_verified  = models.BooleanField(default=False)
	is_active	 = models.BooleanField(default=True)
	is_staff 	 = models.BooleanField(default=False)
	created_at   = models.DateTimeField(auto_now_add=True)
	updated_at   = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	class Meta:
		ordering  = ['-created_at']
		verbose_name_plural = 'User'
	
	def __str__(self):
		return self.email
