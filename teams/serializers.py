from rest_framework import serializers
from .models import Team
from users.models import User

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'creation_time', 'admin','members']
        read_only_fields = ['id', 'creation_time']
        
    def validate_name(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Name cannot exceed 64 characters")
        
        elif len(value) == 0:
            raise serializers.ValidationError("Name cannot accept empty values")
        return value
        
    def validate_description(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("Description cannot exceed 128 characters")
        
        elif len(value) == 0:
            raise serializers.ValidationError("Description cannot be empty")
        return value

class TeamCreateSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Team
        fields = ['name', 'description', 'admin']
        
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

class TeamUpdateSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    
    class Meta:
        model = Team
        fields = ['name', 'description', 'admin']
        
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

class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'display_name']