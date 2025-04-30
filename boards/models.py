from django.db import models

# Create your models here.
from django.db import models
import uuid
from project_planner.teams.models import Team
from project_planner.users.models import User

class Board(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=128, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='boards')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    creation_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('name', 'team')
    
    def __str__(self):
        return f"{self.name} ({self.team.name})"

class Task(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=128, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='OPEN')
    creation_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('title', 'board')
    
    def __str__(self):
        return f"{self.title} ({self.board.name})"