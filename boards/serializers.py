from rest_framework import serializers
from .models import Board, Task
from project_planner.teams.models import Team
from project_planner.users.models import User

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'team', 'status', 'creation_time', 'end_time']
        read_only_fields = ['id', 'creation_time', 'end_time', 'status']
        
    def validate_name(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Name cannot exceed 64 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Name cannot be empty")
        return value
        
    def validate_description(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("Description cannot exceed 128 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Description cannot be empty")
        return value
    
    def validate_status(self, value):
        if value not in ['OPEN', 'IN_PROGRESS', 'COMPLETE']:
            raise serializers.ValidationError("Status must be one of: OPEN, IN_PROGRESS, COMPLETE")
        return value

class BoardCreateSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        source='team',
        queryset=Team.objects.all()
    )
    
    class Meta:
        model = Board
        fields = ['name', 'description', 'team_id']
        
    def validate_name(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Name cannot exceed 64 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Name cannot empty value")
        return value
        
    def validate_description(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("Description cannot exceed 128 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Description cannot be empty")
        return value
        
    def validate(self, data):
        # Check uniqueness of board name for the team
        team = data.get('team')
        name = data.get('name')
        if Board.objects.filter(team=team, name=name).exists():
            raise serializers.ValidationError("Board name must be unique for a team")
        return data

class TaskCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'user_id']
        
    def validate_title(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Title cannot exceed 64 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Title cannot be empty")
        return value
        
    def validate_description(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("Description cannot exceed 128 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Description cannot be empty")
        return value
        
    def validate(self, data):
        # Title uniqueness for a board is handled by the model's unique_together constraint
        return data

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']
        
    def validate_status(self, value):
        if value not in ['OPEN', 'IN_PROGRESS', 'COMPLETE']:
            raise serializers.ValidationError("Status must be one of: OPEN, IN_PROGRESS, COMPLETE")
        return value

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']
