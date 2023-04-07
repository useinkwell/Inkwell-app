Client Websocket connection
===========================
The client websocket connection is used to establish realtime connection with the server for receiving instantaneous user notifications, without need for checking the database periodically or page refresh. The fundamental requirements are:
	- The websocket domain	(e.g ws://127.0.0.1)
	- The endpoint		(e.g /ws/)
	- The user access_token earlier obtained as explained :ref:`here<login>`.


The endpoint used to establish client-server websocket connection is **/ws/**

Assuming we're running the server on the localhost **(127.0.0.1)** and the user's access_token is **123456789**, in order to establish a client-server websocket connection we would create a websocket instance on the client and initialize it with the full path:	**ws://127.0.0.1/ws/123456789/**


Here's a simple node script to create a client which can connect to the server via websocket (you can quickly execute a javascript file in the node interactive shell with **.load <script-name>** e.g .load my_script.js ):

.. code-block:: console

	//import the WebSocket package
	const WebSocket = require('ws');

	//create socket, assuming access_token is 123456789
	const notifySocket = new WebSocket('ws://127.0.0.1:8000/ws/123456789/');


	//add event for what should happen when data is received from the backend
	notifySocket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		if (data.message){
		    console.log('Message received: ' + data.message);
		}
	}


	//add function for sending data to the backend
	function send_message(message){

		notifySocket.send(JSON.stringify({
						'message': message
					}));
	}

	console.log('established websocket connection')


Although the above example shows how to retreive the 'message' string sent in the websocket data, there's further information sent from the server. Here's a breakdown of each piece of information sent and their underlying usage:
	- **message**: The default notification message, prepared from the server. e.g "Oliver created a new post".
	- **action**: The *type* of action the notification represents. e.g **post, comment, reaction, following**
	- **action_id**: The id of the action (if action is **post**, then this is the post id)
	- **by_user**: The username of the user who did something to cause the notification (e.g liking someone's comment)
	- **action_content**: The string content of the action (for cases where content is created by the action -- such as the emoji in a reaction)
	- **affected**: The *type* of content acted on. ( **post/comment** )
	- **affected_id**: The id of the content acted on (if affected_id is **comment**, then this is the comment id )
	
	As a case study if John reacts to the current authenticated user's comment with a "laugh" emoji, the data received by the client would look like this (assume arbitrary numbers for the IDs):
	
	- "message": "John reacted to your comment",
	- "action": "reaction",
	- "action_id": "23",
	- "by_user": "John",
	- "action_content": "laugh",
	- "affected": "comment",
	- "affected_id": "79"
	
Using all these info, a custom notification message can be created at the client side (for instance instead of the default "John reacted to your comment", the received details can be used to fetch the emoji from the database and create a more graphically detailed notification).

	
	
	
	
	
	
	
	
	
            
            
            
