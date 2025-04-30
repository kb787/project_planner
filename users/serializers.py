from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'display_name', 'creation_time']
        read_only_fields = ['id', 'creation_time']
        
    def validate_name(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Name cannot exceed 64 characters")
        
        elif len(value) == 0 :
            raise serializers.ValidationError("Name cannot be empty") 
        return value
        
    def validate_display_name(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("Display name cannot exceed 128 characters")
        
        elif len(value) == 0:
            raise serializers.ValidationError("Name cannot be empty")
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'display_name']
        
    def validate_name(self, value):
        if len(value) > 64:
            raise serializers.ValidationError("Name cannot exceed 64 characters")
        
        elif len(value) == 0:
            raise serializers.ValidationError("Name cannot be empty") 
        return value
        
        
    def validate_display_name(self, value):
        if len(value) > 128:  # Create has 64 char limit
            raise serializers.ValidationError("Display name cannot exceed 64 characters")
        elif len(value) == 0:
            raise serializers.ValidationError("Display name cannot be empty")
        return value

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','display_name']
        
    def validate_name(self,value):
        if len(value) > 64:
             raise serializers.ValidationError("Name cannot exceed 64 characters")   
         
        elif len(value) == 0:
             raise serializers.ValidationError("New updated name cannot be empty") 
        
    def validate_display_name(self, value):
        if len(value) > 128:  # Update has 128 char limit
            raise serializers.ValidationError("Display name cannot exceed 128 characters")
        
        elif len(value) == 0:
            raise serializers.ValidationError("New updated display_name cannot be empty")
        return value

class UserDescribeSerializer(serializers.ModelSerializer):
    # description = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['name', 'display_name', 'creation_time']
        
    def get_description(self, obj):
        return f"User description for {obj.display_name,obj.name,obj.creation_time}"

class UserTeamSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    creation_time = serializers.DateTimeField()