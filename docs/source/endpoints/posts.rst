Posts
=====
Interact with posts in the database.

List All Posts
-----------------
| **endpoint:** /posts/
| **method:** GET
| **requires authentication:** no

Description: Returns all posts.

Path Parameters: None
	
Query parameters:
	| **page:** The page number of the paginated result.
	| **page_size:** The number of posts to return per page in the paginated result. Default is 3. Maximum is 50.
	| **search:** Search keyword for filtering the results. If empty, all the posts are returned.
	| **filter:** The basis for filtering the results based on the search keyword. Options are **title, category, author, hashtag**.

Request Body:
	Required fields: None.
		
	Optional fields: None.


Create Post
-----------
| **endpoint:** /posts/
| **method:** POST
| **requires authentication:** yes

Description: Creates a new post with current authenticated user as the post owner.

Path Parameters: None
	
Query parameters: None

Request Body:
	Required fields:
		| **title:** The title of the post.
		| **content:** The text content of the post.
		| **image:** The image *file* attached to the post (in the future, this would be an optional field but as of the time of creating this documentation, an image file is required).
		
	Optional fields:
		| **category:** The post category.
		| **hashtags:** Hashtags associated with the post.
		

View Post
-----------
| **endpoint:** /post/<post_id>/
| **method:** GET
| **requires authentication:** no

Description: Returns the post with the specified post id.

Path Parameters:
	**post_id** (integer): The id of the post.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.


Update Post
-----------
| **endpoint:** /post/<post_id>/
| **method:** PUT
| **requires authentication:** yes, and current authenticated user must be the post owner

Description: Updates the post with the specified post id.

Path Parameters:
	**post_id** (integer): The id of the post.
	
Query parameters: None

Request Body:
	Required fields:
		| **title:** The title of the post.
		| **content:** The text content of the post.
		
	Optional fields:
		| **category** (string): The post category.
		| **hashtags** (string): Hashtags associated with the post.
		
		
Delete Post
-----------
| **endpoint:** /post/<post_id>/
| **method:** DELETE
| **requires authentication:** yes, and current authenticated user must be the post owner

Description: Deletes the post with the specified post id.

Path Parameters:
	**post_id** (integer): The id of the post.
	
Query parameters: None

Request Body:
	Required fields: None.
		
	Optional fields: None.
	
	
	
	
	
	

