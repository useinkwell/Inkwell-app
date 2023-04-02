Authentication
==============
The API makes use of JWT (JSON Web Tokens) for its user authentication. In a nutshell, this means in order to use an authenticated endpoint you need to apply a valid **access token**. This is gotten on user registration and can also be attained with the user login details. Bear in mind that the access token expires after a set period and must be refreshed using the **refresh token**. The refresh token is also issued when requesting for tokens using the user login details, and has a much longer period before expiry.

To authenticate an endpoint when making a request, simply set the Authorization setting in the request headers as shown below:

headers = {
  'Authorization': 'Bearer <access token>'
  
}


User Registration
-----------------
| **endpoint:** /register/
| **method:** POST
| **requires authentication:** no

Description: Creates a new user with the submitted info and returns the user access token and refresh token.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields:
		| **email:** The email of the new user
		| **password:** The desired user password
		| **user_name:** The desired username
		| **first_name:** User first name
		| **last_name:** User last name
		| **gender:** Gender of the new user
		
	Optional fields: None.


.. _login:
Obtain User Access Token
------------------------
| **endpoint:** /token/
| **method:** POST
| **requires authentication:** no

Description: Returns a new access token and refresh token for an existing user.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields:
		| **email:** The user email
		| **password:** The user password
		
	Optional fields: None.


Refresh User Access Token
-------------------------
| **endpoint:** /token/refresh/
| **method:** POST
| **requires authentication:** no

Description: Refreshes the specified user access token.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields:
		| **refresh:** The specified access token that needs to be refreshed.
		
	Optional fields: None.
	



