from django.db import models

# Create your models here.
import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=64,unique=True)
    display_name = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name