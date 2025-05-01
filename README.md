Welcome to API Docs of Project Planner Using Django

a. Users API

     1. Get User List , (Fetches List of All Users)
     
           API Endpoint : api/users/list-user/
           Method Type : GET
        
           
          
     2. Create New User , (Adds a new user to db)
           API Endpoint : api/users/create-user/
           Method Type : POST
           Sample Payload :
           {
                "name":"knightkb787",
                 "display_name":"Karan_Bhanushali_Dama"
            }
           “name” : CharField . “display_name”:CharField

           Other Validations :
           1. “name”  field cannot exceed 64 characters and cannot be of 0 length
           2. “display_name” field cannot exceed 128 characters and cannot be of 0 length
           3. “name” field should be unique for different users

    
    3. Describe User (Provides Details of specific user)

          API Endpoint : api/users/describe-user/
          Method Type : POST
          Mandatory Field : “id” (User search based on id)
          Sample Payload : 
          {
            "id":"40fa77e8-ea47-4403-b739-2ce79b103eaf"
          } 


    

     4. Get User Teams (Provides teams data associated with user)
   
          API Endpoint : api/users/user-teams/
          Method Type : POST
          Mandatory Field : “id” (User search based on id)
          Sample Payload : 
          {
            "id":"9ba68452-0880-41ce-af9e-9aef53ddf56e"
          } 
     

     5. Update User , (Updates existing user data)
           API Endpoint : api/users/update-user/ 
           Method Type : POST
           Sample Payload :
            {
              "id":"9ba68452-0880-41ce-af9e-9aef53ddf56e",
              "name":"Mike",
              "display_name":"Kundan_Patel"
           }
           Mandatory Fields :- 
          “id” : Char Field    “name” : Char Field . “display_name”:Char Field

          Other Validations :
          1. “name”  field cannot exceed 64 characters and cannot be of 0 length
          2. “display_name” field cannot exceed 128 characters and cannot be of 0 length
          3. “name” field should be unique for different users

b. Teams API

     1. Get Teams List , (Fetches List of All Available Teams)
           API Endpoint : api/teams/list-team/
           Method Type : GET

     2. Create New Team(Creates a new team in db)
           API Endpoint : api/teams/create-team/
           Method Type : POST 
           Sample Payload : 
            {
              "name": "Team 25",
              "description": "This is a description for Team 25.",
              "admin": "39e13e32-b52b-4b3a-af71-e11542d7007c"
            }
           Mandatory Fields  :
           "name" : Char Field, "description" : Char Field , "admin": Char Field
           (Id of user to be declared as admin)

           Other Validations :
           1. "name" field value cannot exceed 64 characters nor it can have empty characters
           2. "description" field value cannot exceed 128 characters not it have empty characters
           3. "name" field must be unique for different documents

     3. Describe Team(Provides detail about team)
           API Endpoint : api/teams/describe-team/
           Method Type : POST
           Sample Payload : 
            {
              "id": "f53a56f0-a47e-403e-b428-758a8d2e2d66"
            }
           Mandatory Field : "id"(Id of team whose data is to be fetched)

     4. Get Team Users (Provides user data associated with team)
           API Endpoint :- api/team/team-users/
           Method Type : POST
           Mandatory Field : "id" ("Id" of team whose user-data to be fetched)
           Sample Payload :- 
            {
              "id":"bb5544d3-3f70-4cec-8ff7-d0c924716bec"
            }

     5. Update-Team (Updates team data)
           API Endpoint : /api/teams/update-team/
           Method Type : POST
           Sample Payload : 
            {
              "id":"f53a56f0-a47e-403e-b428-758a8d2e2d66",
              "name":"KnightTeam",
              "description":"DeskKnight"
            }
           Mandatory Fields  :
           "id" : Char Field, "name" : Char Field, "description" : Char Field , "admin": Char Field
           (Id of team whose data to be updated )

           Other Validations :
           1. "name" field value cannot exceed 64 characters nor it can have empty characters
           2. "description" field value cannot exceed 128 characters not it have empty characters

     6. Add-User-To-Team (Adds a user to team)
           API Endpoint :- /api/teams/add-users-team/
           Method Type :- POST
           Sample Payload :- 
            {
              "team_id":"edeea0d6-83bb-4d08-b759-a5296cd349ce",
              "user_ids":["0e56edea-6247-4374-9342-2f2eb4d47190","d628ca02-671e-41ee-9393-0952070f6143"]
            }
           Mandatory Fields :
           "team_id" : Char Field, Id of team in which user is to be added
           "user_ids" :  Char Array Field, Group of user_id to be added in the specified team   

           Other Validations :
           If user_ids array length exceeds 50 then new user cannot be added to team

     7. Remove-User-From-Team (Removes Specified Users from Team)
           API Endpoint : api/teams/remove-users-team/
           Method Type : POST
           Sample Payload : 
            {
              "team_id":"a681d92a-81bf-42b0-aee6-3d64a12dc4cf",
              "user_ids":["e0dc79de-aa54-4637-b81d-1a120c8c715e","ed7ffc44-4e11-402e-82a5-cc353b5745d9"]
            }
           Mandatory Fields :-
           "team_id" : Char Field, Id of team in which user is to be removed
           "user_ids" :  Char Array Field, Group of user_id to be removed from the specified team

c. Boards API

     1. Get Boards List , (Fetches Available Boards for specified team)
           API Endpoint :- api/boards/list-board/
           Method Type :- POST
           Sample Payload :-
            {
              "id":"71814df6-014f-4925-b69d-93affb04bb38"
            } 
           Mandatory Field :- 
           "id" : Char Field (Id of team whose corresponding board has to be found)

     2. Create New Board (Creates new board in db)
           API Endpoint :- api/boards/create-board/
           Method Type :- POST 
           Sample Payload :- 
            {
              "name":"Next_For_Team",
              "description":"Board_Created_for_Team",
              "team_id": "71814df6-014f-4925-b69d-93affb04bb38"
            }  
           Mandatory Field :-
           "name" :- Char Field , "description" :- Char Field, "team-id" :- Char Field 
           Other Validations :-
           1. "name" field character length cannot exceed 64 and cannot be empty
           2. "description" field character length cannot exceed 128 and cannot be empty 
           3. Every board name should be unique for a team 

     3. Close Board (Closes an open board)
           API Endpoint :- api/boards/close-board
           Method Type :- POST
           Sample Payload :- 
            {
              "id":"d7164f9f-0cde-4784-8729-f3e11c4d4f5c"
            }
           Mandatory Field :- "id" – Char Type(Id of board to be closed)
           Other Validations :- 
           1. Before closing a board it checks for incomplete tasks if incomplete tasks exists then a board cannot be closed 

     4. Add Task (Adds a task to board)
           API Endpoint :- api/boards/task/add
           Method Type :- POST   
           Sample Payload :- 
            {
              "board_id":"fa3982f0-04c0-4ea6-9c5f-3155fb3e24c9",
              "title":"Do coding",
              "description":"Practice Java",
              "user_id":"815caab5-3ddb-4833-b75b-023d512a4ce7"
            }
           Mandatory Fields :-
           "board_id" : Char Field (Id of board in which task to be added), "title" : Char Field (Task Title), "description" : Char Field (Task Description) 

           Other Validations :-
           1. If board is not open then no tasks can be added to it
           2. Task Title should be unique

     5. Update Status(Used to update the status of created tasks)
           API Endpoint :- /api/boards/task/update-task/
           Method Type :- POST

           Sample Payload :- 
            {
              "id": "2c140ae3-b60f-467e-af51-3bfcea7afd03",
              "status":"COMPLETE"
            }

           Mandatory Fields :- 
           "id" : Char Field , (Id of task to update status)
           "status" : Char Field, (Status to update)

     6. Export Tasks (Exports task data, status, creation_time)
           API Endpoint :- /api/boards/export-board/
           Method : POST
           Sample Payload : 
            {
              "id":"fa3982f0-04c0-4ea6-9c5f-3155fb3e24c9"
            }
           Mandatory Field :- "id" (Id field of task to be exported)
