Following
=========
Interact with user following relationships in the database.


List Followers
--------------
| **endpoint:** /following/followers/
| **method:** GET
| **requires authentication:** yes

Description: Returns a list of the usernames of all the current authenticated user's followers.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

List Followed Users
-------------------
| **endpoint:** /following/followed/
| **method:** GET
| **requires authentication:** yes

Description: Returns a list of the usernames of all the users followed by the current authenticated user.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

Follow User
-----------
| **endpoint:** /following/follow/<other_user>/
| **method:** POST
| **requires authentication:** yes

Description: Makes the current authenticated user to follow the specified user

Path Parameters:
	**other_user** (string): The username of the user to be followed by the currently authenticated user.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

Unfollow User
-------------
| **endpoint:** /following/unfollow/<other_user>/
| **method:** POST
| **requires authentication:** yes

Description: Makes the current authenticated user to unfollow the specified user

Path Parameters:
	**other_user** (string): The username of the user to be unfollowed by the current authenticated user.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

Check Followership
------------------
| **endpoint:** /following/check/<other_user>/
| **method:** GET
| **requires authentication:** yes

Description: Returns the bi-directional status of the following relationship between the current authenticated user and the specified user. In otherwords it tells which user follows the other.

Path Parameters:
	**other_user** (string): The username of the user whose following relationship is to be checked with the current authenticated user.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	
		
		
		
	
	


