from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer, 
    UserDescribeSerializer,
    UserTeamSerializer
)
from teams.models import Team

class UserBase:
    """Base interface implementation for API's to manage users."""
    
    def create_user(self, request: str) -> str:
        """Create a new user."""
        try:
            data = json.loads(request)
            serializer = UserCreateSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return json.dumps({"id": str(user.id)})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_users(self) -> str:
        """List all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return json.dumps([{
            "id": user["id"],
            "name": user["name"],
            "display_name": user["display_name"],
            "creation_time": user["creation_time"]
        } for user in serializer.data])
    
    def describe_user(self, request: str) -> str:
        """Describe a specific user."""
        try:
            data = json.loads(request)
            print("Frontend-Data",data)
            user_id = data.get("id")
            if not user_id:
                raise ValueError("User ID is required")
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValueError(f"User with ID {user_id} does not exist")
            
            serializer = UserDescribeSerializer(user)
            return json.dumps(serializer.data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_user(self, request: str) -> str:
        """Update a user."""
        try:
            data = json.loads(request)
            print(data,"data")
            user_id = data.get("id")
            user_data = data
            name = user_data.get("name") 
            display_name  = user_data.get("display_name")
            print(name,"name value received")
            print(display_name,"display_name value received")
            print(user_data,"user_data")
            if not user_id or not name or not display_name:
                raise ValueError("User ID , name , display_name all are required")
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValueError(f"User with ID {user_id} does not exist")
            
            # User name cannot be updated
            serializer = UserUpdateSerializer(user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return json.dumps({"success": True})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def get_user_teams(self, request: str) -> str:
        """Get teams for a user."""
        try:
            data = json.loads(request)
            user_id = data.get("id")
            if not user_id:
                raise ValueError("User ID is required")
            
            try:
                user = User.objects.get(id=user_id)
                print(user,"userObject")
            except User.DoesNotExist:
                raise ValueError(f"User with ID {user_id} does not exist")
            
            teams = user.teams.all()
            print(teams,"teamFromUser")
            teams_data = []
            for team in teams:
                teams_data.append({
                    "name": team.name,
                    "description": team.description,
                    "creation_time": team.creation_time.isoformat()
                })
            print(teams_data,'team_data-after-iteration')
            return json.dumps(teams_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

class UserCreateView(APIView, UserBase):
    def post(self, request):
        try:
            print(request,'payload-data-create-user')
            result = self.create_user(json.dumps(request.data))
            print(result,'creation-output')
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView, UserBase):
    def get(self, request):
        try:
            result = self.list_users()
            print(result,'user_list')
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDescribeView(APIView, UserBase):
    def post(self, request):
        try:
            result = self.describe_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView, UserBase):
    def post(self, request):
        try:
            result = self.update_user(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserTeamsView(APIView, UserBase):
    def post(self, request):
        try:
            result = self.get_user_teams(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


