from django.shortcuts import render
import string
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Team
from users.models import User
from .serializers import (
    TeamSerializer, 
    TeamCreateSerializer, 
    TeamUpdateSerializer,
    TeamUserSerializer
)

class TeamBase:
    """Base interface implementation for API's to manage teams."""
    
    def create_team(self, request: str) -> str:
        """Create a new team."""
        try:
            data = json.loads(request)
            serializer = TeamCreateSerializer(data=data)
            if serializer.is_valid():
                team = serializer.save()
                # Add admin as a member
                team.members.add(team.admin)
                return json.dumps({"id": str(team.id)})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_teams(self) -> str:
        """List all teams."""
        teams = Team.objects.all()
        print(teams,'teams-data')
        teams_data = []
        for team in teams:
            teams_data.append({
                "id":str(team.id),
                "name": team.name,
                "description": team.description,
                "creation_time": team.creation_time.isoformat(),
                "admin": str(team.admin.id)
            })
        print(teams_data,'after-push-teams-data')    
        return json.dumps(teams_data)
    
    def describe_team(self, request: str) -> str:
        """Describe a specific team."""
        try:
            data = json.loads(request)
            print('frontend-payload_teams',data)
            team_id = data.get("id")
            if not team_id:
                raise ValueError("Team ID is required")
            
            try:
                team = Team.objects.get(id=team_id)
                print(team,'Team_Value_Fetched')
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            return json.dumps({
                "name": team.name,
                "description": team.description,
                "creation_time": team.creation_time.isoformat(),
                "admin": str(team.admin.id)
            })
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_team(self, request: str) -> str:
        """Update a team."""
        try:
            data = json.loads(request)
            print(data,'frontend_data')
            team_id = data.get("id")
            team_data = data
            print(team_id,'teamId',team_data,'teamData')            
            if not team_id or not team_data:
                raise ValueError("Team ID and team data are required")
            
            try:
                team = Team.objects.get(id=team_id)
                print(team,'teamFetched')
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            serializer = TeamUpdateSerializer(team, data=team_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return json.dumps({"success": True})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def add_users_to_team(self, request: str) -> str:
        """Add users to a team."""
        try:
            data = json.loads(request)
            print(data,'frontend_payload_adding_users')
            team_id = data.get("team_id")
            user_ids = data.get("user_ids")
            print(team_id,'teamId Fetched')
            print(user_ids,'userId Fetched')
            if not team_id:
                raise ValueError("Team ID is required")
            elif not user_ids:
                raise ValueError("User IDs are required")
            try:
                team = Team.objects.get(id=team_id)
                print(team,'team_value_for_add_users')
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            # Cap the max users that can be added to 50
            current_members = team.members.count()
            if current_members + len(user_ids) > 50:
                raise ValueError("Cannot add more than 50 users to a team")
            
            # Add users to team
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    team.members.add(user)
                except User.DoesNotExist:
                    raise ValueError(f"User with ID {user_id} does not exist")
            
            return json.dumps({"success": True})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def remove_users_from_team(self, request: str) -> str:
        """Remove users from a team."""
        try:
            data = json.loads(request)
            print(data,'frontend_payload_removing_users')
            team_id = data.get("team_id")
            user_ids = data.get("user_ids")
            print(team_id,'teamId Fetched')
            print(user_ids,'userId Fetched') 
            if not team_id:
                raise ValueError("Team ID is required")
            if not user_ids:
                raise ValueError("User IDs are required")
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            # Remove users from team
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    # Don't remove the admin
                    if user == team.admin:
                        raise ValueError("Cannot remove the team admin")
                    team.members.remove(user)
                except User.DoesNotExist:
                    raise ValueError(f"User with ID {user_id} does not exist")
            
            return json.dumps({"success": True})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_team_users(self, request: str) -> str:
        """List users in a team."""
        try:
            data = json.loads(request)
            team_id = data.get("id")
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            users = team.members.all()
            serializer = TeamUserSerializer(users, many=True)
            return json.dumps(serializer.data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

class TeamCreateView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.create_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamListView(APIView, TeamBase):
    def get(self, request):
        try:
            result = self.list_teams()
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamDescribeView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.describe_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamUpdateView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.update_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamAddUsersView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.add_users_to_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamRemoveUsersView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.remove_users_from_team(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamUsersView(APIView, TeamBase):
    def post(self, request):
        try:
            result = self.list_team_users(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND) 
       