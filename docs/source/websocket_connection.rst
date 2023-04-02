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

	//create chatsocket, assuming access_token is 123456789
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

