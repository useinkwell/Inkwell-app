Account Info
============
View account info. If checking for the currently authenticated user, it returns all information including user credentials (such as access tokens). If checking for another user, it returns only non-sensitive account info. Checking account info of another user is restricted to admin only.

Current User
------------
| **endpoint:** /account/
| **method:** GET
| **requires authentication:** yes

Description: Returns the account info of the currently authenticated user.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields: None
		
	Optional fields: None


Other User 
----------
| **endpoint:** /account/<username>/
| **method:** GET
| **requires authentication:** yes, plus admin privilege

Description: Returns the account info of any user with the specified username. This endpoint is restricted for admin use only.

Path Parameters:
	**username:** The username of other user
	
Query parameters: None

Request Body:
	Required fields: None
		
	Optional fields: None

