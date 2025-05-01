from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
import os
from django.conf import settings
from .models import Board, Task
from teams.models import Team
from .serializers import (
    BoardSerializer, 
    BoardCreateSerializer, 
    TaskCreateSerializer,
    TaskStatusUpdateSerializer,
    BoardListSerializer
)

class ProjectBoardBase:
    """Implementation of the ProjectBoardBase interface."""
    
    def create_board(self, request: str) -> str:
        """Create a new project board."""
        try:
            data = json.loads(request)
            print(data,'frontend-payload-board-creation')
            # Formatting data to match serializer expectations
            formatted_data = {
                'name': data.get('name'),
                'description': data.get('description'),
                'team_id': data.get('team_id')
            }
            print(formatted_data,'formatted-data')
            if not formatted_data['team_id'] or not formatted_data['name'] or not formatted_data['description']:
                raise ValueError("Team ID,Board Name,Board Description is required")
            serializer = BoardCreateSerializer(data=formatted_data)
            if serializer.is_valid():
                board = serializer.save()
                return json.dumps({"id": str(board.id)})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def close_board(self, request: str) -> str:
        """Close a project board."""
        try:
            data = json.loads(request)
            print(data,'frontend-payload-board-closure')
            board_id = data.get("id")
            if not board_id:
                raise ValueError("Board ID is required")
            
            try:
                board = Board.objects.get(id=board_id)
                print(board,'board-object-fetched')
            except Board.DoesNotExist:
                raise ValueError(f"Board with ID {board_id} does not exist")
            
            # Check if all tasks are complete
            incomplete_tasks = board.tasks.exclude(status='COMPLETE').count()
            print(incomplete_tasks,'incomplete-tasks-count')
            if incomplete_tasks > 0:
                raise ValueError("Cannot close board with incomplete tasks")
            
            # Close the board
            board.status = 'CLOSED'
            board.end_time = datetime.now()
            board.save()
            
            return json.dumps({"success": True})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def add_task(self, request: str) -> str:
        """Add a task to a board."""
        try:
            data = json.loads(request)
            print(data,'frontend-payload-add-task')
            board_id = data.get("board_id")
            print(board_id,'board-id-from-payload')
            if not board_id:
                raise ValueError("Board ID is required")
            
            try:
                board = Board.objects.get(id=board_id)
                print(board,'board-object-fetched')
            except Board.DoesNotExist:
                raise ValueError(f"Board with ID {board_id} does not exist")
            
            # Check if board is open
            if board.status != 'OPEN':
                raise ValueError("Can only add tasks to an OPEN board")
            
            # Create the task
            task_data = {
                'title': data.get('title'),
                'description': data.get('description'),
                'user_id': data.get('user_id')
            }
            print(task_data,'task-data-from-data')            
            serializer = TaskCreateSerializer(data=task_data)
            if serializer.is_valid():
                task = serializer.save(board=board)
                return json.dumps({"id": str(task.id)})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def update_task_status(self, request: str) -> str:
        """Update the status of a task."""
        try:
            data = json.loads(request)
            print(data,'frontend-payload-update-task-status')
            task_id = data.get("id")
            status = data.get("status")
            
            if not task_id or not status:
                raise ValueError("Task ID and status are required")
            
            try:
                task = Task.objects.get(id=task_id)
                print(task,'task-object-fetched')
            except Task.DoesNotExist:
                raise ValueError(f"Task with ID {task_id} does not exist")
            
            # Update the task status
            serializer = TaskStatusUpdateSerializer(task, data={"status": status})
            if serializer.is_valid():
                serializer.save()
                return json.dumps({"success": True})
            else:
                raise ValueError(json.dumps(serializer.errors))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def list_boards(self, request: str) -> str:
        """List all open boards for a team."""
        try:
            data = json.loads(request)
            print(data,'frontend-payload-list-boards')
            team_id = data.get("id")
            print(team_id,'team-id-from-payload')
            
            if not team_id:
                raise ValueError("Team ID is required")
            
            try:
                team = Team.objects.get(id=team_id)
                print(team,'team-fetched-id')
            except Team.DoesNotExist:
                raise ValueError(f"Team with ID {team_id} does not exist")
            
            # Get all open boards for the team
            boards = Board.objects.filter(team=team, status='OPEN')
            serializer = BoardListSerializer(boards, many=True)
            print(serializer,'serializer-final')
            return json.dumps(serializer.data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def export_board(self, request: str) -> str:
        """Export a board to a text file."""
        try:
            data = json.loads(request)
            board_id = data.get("id")
            
            if not board_id:
                raise ValueError("Board ID is required")
            
            try:
                board = Board.objects.get(id=board_id)
                print(board,'board-object-fetched')
            except Board.DoesNotExist:
                raise ValueError(f"Board with ID {board_id} does not exist")
            
            # Create the output directory if it doesn't exist
            out_dir = os.path.join(settings.BASE_DIR, 'out')
            os.makedirs(out_dir, exist_ok=True)
            
            # Generate a filename
            filename = f"board_{board.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = os.path.join(out_dir, filename)
            
            # Create a formatted board export
            with open(file_path, 'w') as f:
                f.write(f"=== BOARD: {board.name} ===\n")
                f.write(f"Description: {board.description}\n")
                f.write(f"Status: {board.status}\n")
                f.write(f"Created: {board.creation_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                if board.end_time:
                    f.write(f"Completed: {board.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Team: {board.team.name}\n\n")
                
                f.write("=== TASKS ===\n")
                tasks = board.tasks.all().order_by('status', 'creation_time')
                print(tasks,'all-tasks-fetched')
                
                for task in tasks:
                    f.write(f"\n--- Task: {task.title} ---\n")
                    f.write(f"Status: {task.status}\n")
                    f.write(f"Assigned to: {task.user.display_name}\n")
                    f.write(f"Created: {task.creation_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Description: {task.description}\n")
            
            return json.dumps({"out_file": filename})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

class BoardCreateView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.create_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardCloseView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.close_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskAddView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.add_task(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskUpdateStatusView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.update_task_status(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardListView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.list_boards(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BoardExportView(APIView, ProjectBoardBase):
    def post(self, request):
        try:
            result = self.export_board(json.dumps(request.data))
            return Response(json.loads(result), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)