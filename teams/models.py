from django.db import models

# Create your models here.
from django.db import models
import uuid
from project_planner.users.models import User

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=128, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_teams')
    members = models.ManyToManyField(User, related_name='teams')
    
    def __str__(self):
        return self.name