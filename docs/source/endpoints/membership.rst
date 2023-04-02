Membership
============
View account membership. If checking for the currently authenticated user, it returns the membership of the current user. Checking account membership of another user is restricted to admin only.

Current User Membership
-----------------------
| **endpoint:** /membership/
| **method:** GET
| **requires authentication:** yes

Description: Returns the account membership of the currently authenticated user.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields: None
	
	Optional fields: None


Other User Membership
---------------------
| **endpoint:** /account/<user id>/
| **method:** GET
| **requires authentication:** yes, plus admin privilege

Description: Returns the account membership of any user with the specified user id. This endpoint is restricted for admin use only.

Path Parameters:
	**user id:** The id of other user
	
Query parameters: None

Request Body:
	Required fields: None
		
	Optional fields: None

