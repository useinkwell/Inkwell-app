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

Description: Creates a new user with the submitted info and returns the user access token and refresh token. At this point, the new user account is inactive and the tokens cannot be used yet. However, an email containing the account activation URL is sent to the provided user email for email verification purposes. Opening the URL received in the email activates the profile after which the access and refresh tokens become usable. An "email verified" page/route (can even be the homepage) should be implemented at the client side for redirecting the browser to it once the user profile is activated. This route (decided at the client side) would then be implemented at the server side to redirect it accordingly.

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
	

Forgot Password
-------------------------
| **endpoint:** /forgot_password/
| **method:** POST
| **requires authentication:** no

Description: Sends an password reset URL to the given user email if a user with such email exists. A "password reset" page/route should be implemented at the client side, and this route would be used at the server side when sending the email so that when the password reset URL is clicked it directs to that designated password reset page at the client side. The requirements for the password reset page would be discussed in the "Reset Password" endpoint below.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields:
		| **email:** The specified user email.
		
	Optional fields: None.
	

Reset Password
-------------------------
| **endpoint:** /reset_password/
| **method:** POST
| **requires authentication:** no

Description: Resets the user password with the specified new password as well as the encrypted access_token (x_access_token) received as query parameter from the password reset URL sent to the user email. This comes after using the "Forgot Password" endpoint above. As discussed briefly in the "Forgot Password" endpoint, a "password reset" page/route should be implemented at the client side and this route would be used at the server side when sending the email so that when the password reset URL is clicked it directs to that designated password reset page at the client side (while keeping the x_access_token query parameter attached). The password reset page must have a **password** and **password2** field for password confirmation at the client side, and the **x_access_token** query parameter automatically added in the URL from the password reset email should be left untouched. Just to be clear, it is the "password reset" page at the client side which submits a POST request to this "Reset Password" endpoint.
Bear in mind that once a successful form submission is done, the password reset URL received in the email can no longer be used. Hence it is advisable to implement necessary form validation at the client side (even though it would still be validated at the server side for full security).

Path Parameters: None
	
Query parameters:
	**x_access_token**: This is an encrypted JWT access token automatically added in the password reset URL and is the only instance where a query parameter is mandatory.

Request Body:
	Required fields:
		| **password:** The new password.
		| **password2:** The confirmation password. Both must be the same.
		
	Optional fields: None.
	
	


