Reactions
=========
Interact with reactions in the database. A single user can react several times on a particular content, but each reaction must be of unique emoji. What this means in a nutshell is that the user can for example leave a "laugh" and a "surprised" reaction on a particular content, but cannot 'laugh twice' on it.


List All Reactions on post/comment
----------------------------------
| **endpoint** (reactions on post): /react/list/post/<post_id>/
| **endpoint** (reactions on comment): /react/list/comment/<comment_id>/
| **method:** GET
| **requires authentication:** no

Description: Returns all reactions on a post or comment as the case may be.

Path Parameters:
	| **post_id** (integer): The id of the post if using the post endpoint
	| **comment_id** (integer): The id of the comment if using the comment endpoint
	
Query parameters: None.

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

React on post/comment
---------------------
| **endpoint** (react on post): /react/add/post/<post_id>/<emoji>/
| **endpoint** (react on post): /react/add/comment/<comment_id>/<emoji>/
| **method:** POST
| **requires authentication:** yes

Description: Reacts on a post or comment, with the current authenticated user as the reaction owner.

Path Parameters:
	| **post_id** (integer): The id of the post if using the post endpoint
	| **comment_id** (integer): The id of the comment if using the comment endpoint
	| **emoji** (string): The emoji to use in reacting
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	

Remove reaction from post/comment
---------------------------------
| **endpoint** (reaction on post): /react/remove/post/<post_id>/<emoji>/
| **endpoint** (reaction on comment): /react/remove/comment/<comment_id>/<emoji>/
| **method:** POST
| **requires authentication:** yes, and current authenticated user must be the reaction owner

Description: Removes the reaction having specified emoji from the post or comment having the post_id or comment_id respectively.

Path Parameters:
	| **post_id** (integer): The id of the post if using the post endpoint
	| **comment_id** (integer): The id of the comment if using the comment endpoint
	| **emoji** (string): The emoji to be removed
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
		
		
		
		
