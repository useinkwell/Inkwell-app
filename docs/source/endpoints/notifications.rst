Notifications
=============
Interact with user notification history stored in the database. Notifications are automatically created in the database when a websocket event is sent toward the user, whether the user is online or not. This section is strictly about the notifications in the database, not websockets.


List All User Notifications
---------------------------
| **endpoint:** /notification/
| **method:** GET
| **requires authentication:** yes

Description: Returns all the stored notifications of the current authenticated user.

Path Parameters: None
	
Query parameters:
	| **page:** The page number of the paginated result.
	| **page_size:** The number of notifications to return per page in the paginated result. Default is 50. Maximum is 1000.

Request Body:
	Required fields: None.
		
	Optional fields: None.
	
	

View Notification
-----------------
| **endpoint:** /notification/<notification_id>/
| **method:** GET
| **requires authentication:** yes, and current authenticated user must be the notification owner

Description: Returns the notification having the specified notification id.

Path Parameters:
	**notification_id** (integer): The id of the notification.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	


Update Notification
-------------------
| **endpoint:** /notification/<notification_id>/
| **method:** PATCH
| **requires authentication:** yes, and current authenticated user must be the notification owner

Description: Updates the notification with the specified notification id.

Path Parameters:
	**notification_id** (integer): The id of the notification.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields:
		**message** (string): The notification message.
		**is_seen** (boolean): Whether the user has read the notification or not.
		**event_url** (string): URL attributed to this notification. Would typically be used for making it easy to simply click on a notification message in order to immediately navigate to the page of that event, such as the URL of the post in a notification about a new post by a followed user.
		**created_at**: Datetime in the form *2023-03-30T10:27:04.905100Z*
		**user** (integer): The id of the user who owns (received) the notification.
			


Delete Notification
-------------------
| **endpoint:** /notification/<notification_id>/
| **method:** DELETE
| **requires authentication:** yes, and current authenticated user must be the notification owner

Description: Deletes the notification with the specified notification id.

Path Parameters:
	**notification_id** (integer): The id of the notification.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.





	
