from django.db import models
import uuid

class BaseModel(models.Model):
    #uuid field
    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True)
    

        #date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True

