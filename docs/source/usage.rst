Usage
=====

This documentation comprises of two main parts:

:doc:`api_endpoints`

:doc:`websocket_connection`


API Endpoints
-------------
The API endpoints are based on the REST protocol and are simply used for database interaction for viewing, creating, updating and deleting data. Some endpoints are public and accessible to all users (e.g viewing all posts), while others require authentication (e.g making a post).

| The full form of every endpoint takes the structure: <domain><base url><endpoint>
| Example: http://127.0.0.1/api/posts/

Where:
	| **domain:** http://127.0.0.1
	| **base url:** /api
	| **endpoint:** /posts/
	
There are two different base urls:

| **/auth** for the endpoints in the *authentication* category.
| **/api** for the endpoints in all *other* categories (account_info, membership, etc).

Passing data into a request
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The data passed into a request could be any of these 3 types: The request **body**, a **path parameter** or a **query parameter**.
	- Data passed into the request body is synonymous to the data passed on submitting a html form and can either be *required* (must be provided) or *optional*.
	- Path parameters are passed in the URL and take the form **/post/<post_id>/** where **post_id** is the parameter in this scenario. Path parameters are mandatory (required) unless specified otherwise.
	- Query parameters are also passed into the URL but unlike the path parameters, query parameters are completely optional (except in the "Reset Password" endpoint where it is automatically added and crucial). They take the form **/posts/?page=2&page_size=10** where **page** and **page_size** are the query parameters in this scenario.

Authenticating an endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~
For endpoints requiring user authentication, the request headers must be set with the bearer token as explained in :doc:`endpoints/authentication`


Client Websocket Connection
---------------------------
The :doc:`websocket_connection` section covers the steps in enabling live connection from the client to the server via websocket in order for the client to receive instant user notifications.

