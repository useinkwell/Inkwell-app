Comments
========
Interact with comments in the database.

List All comments in a post
---------------------------
| **endpoint:** /comments/post/<post_id>/
| **method:** GET
| **requires authentication:** no

Description: Returns all comments belonging to the post having the specified post id.

Path Parameters:
	**post_id** (integer): The id of the post for which all its comments should be returned.
	
Query parameters:
	| **page:** The page number of the paginated result.
	| **page_size:** The number of comments to return per page in the paginated result. Default is 50. Maximum is 1000.

Request Body:
	Required fields: None.
		
	Optional fields: None.

	
Create Comment
--------------
| **endpoint:** /comments/post/<post_id>/
| **method:** POST
| **requires authentication:** yes

Description: Creates a new comment under the post having specified post id, with the current authenticated user as its owner.

Path Parameters:
	**post_id** (integer): The id of the existing post under which the comment should belong.
	
Query parameters:
	| **content**: The text message contained in the comment.
	| **parent_comment** (integer)(optional): The id of the comment which should be its parent, if making a nested comment. This is equivalent to replying to the parent comment, and not directly to the post. If left out, the created comment would be a direct comment under the post itself.

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

View Comment
------------
| **endpoint:** /comment/<comment_id>/
| **method:** GET
| **requires authentication:** no

Description: Returns the comment with the specified comment id.

Path Parameters:
	**comment_id** (integer): The id of the comment.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.


Update Comment
--------------
| **endpoint:** /comment/<comment_id>/
| **method:** PUT
| **requires authentication:** yes, and current authenticated user must be the comment owner

Description: Updates the comment with the specified comment id.

Path Parameters:
	**comment_id** (integer): The id of the comment.
	
Query parameters: None

Request Body:
	Required fields:
		| **post** (integer): The id of the post which the comment belongs to.
		| **content:** The text content of the comment.
		
	Optional fields:
		| **parent_comment** (integer): The id of the comment which should be its parent, if making a nested comment.
		| **user** (integer): The user id indicating the owner of the comment.
		| **date_posted** (string): The datetime of the post, in the format *2023-03-30T10:22:15Z*
		

Delete Comment
--------------
| **endpoint:** /comment/<comment_id>/
| **method:** DELETE
| **requires authentication:** yes, and current authenticated user must be the comment owner

Description: Deletes the comment with the specified comment id.

Path Parameters:
	**comment_id** (integer): The id of the comment.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
		
		
		
		

