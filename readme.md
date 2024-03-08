A server-client architecture based mock SMTP program.

server.py is a python script running server for a simple email-like service. It uses sockets for network communication, threading for handling multiple clients simultaneously, RSA for public-key cryptography, and SSL for secure connections. Here's a breakdown of what the code does:

    1. **Setup**: The server generates a pair of RSA keys, creates a TCP/IP socket, binds it to a specific address and port, and starts listening for incoming connections. It also sets up an SSL context and wraps the server socket with SSL for secure connections.

    2. **Client handling**: When a client connects, the server starts a new thread to handle the client. This allows the server to handle multiple clients simultaneously. Each client is assigned a unique email address.

    3. **Command processing**: The server receives commands from the client and responds accordingly. The commands include:
   - `HELO`: The server responds with the client's email address.
   - `MAIL FROM:`: The server checks if the sender address matches the client's email address. If it does, the server asks for the recipient email address.
   - `RCPT TO:`: The server checks if the recipient address exists. If it does, the server asks for the message.
   - `DATA:`: The server accepts the message for delivery and sends it to the recipient.
   - `CANCEL`: The server clears the sender and recipient addresses.
   - `RCKEY`: The server sends its public key to the client.
   - `HI`: The server sends a hello message to the client.
   - `QUIT`: The server ends the connection with the client.

    4. **Error handling**: If a connection is aborted by the client, the server handles the `ConnectionAbortedError` and ends the client handling thread. If an unknown command is received, the server responds with 'Unknown Command'.

    5. **Cleanup**: When a client disconnects, the server closes the connection with the client. The server continues to run and accept new connections until it is stopped.


client.py is a python script running client for a simple email-like service. It uses sockets for network communication, threading for sending and receiving messages simultaneously, and SSL for secure connections. Here's a breakdown of what the code does:

    1. **Setup**: The client creates a TCP/IP socket, defines the server address and port, and prints a message indicating it's attempting to connect to the server. It also sets up an SSL context, disables hostname checking and certificate verification, and wraps the client socket with SSL for secure connections.

    2. **Connection**: The client connects to the server using the SSL-enabled socket.

    3. **Message handling**: The client starts two threads: one for receiving messages from the server and one for sending messages to the server. This allows the client to send and receive messages simultaneously.

    4. **Receiving messages**: In the `receive_message` function, the client continuously receives messages from the server and prints them. If the message starts with 'HELO ', the client extracts the email address from the message and prints it. If the message is 'GooodBYE', the client prints 'SERVER SAYS GooodBYE'. For all other messages, the client simply prints 'SERVER SAYS' followed by the message.

    5. **Sending messages**: In the `send_message` function, the client continuously takes input from the user and sends it to the server. If the user enters 'QUIT', the client prints 'Closing the connection', stops receiving messages, and breaks the loop.

    6. **Cleanup**: When the client is done sending messages, it closes the connection with the server.

This client can be used to send and receive messages from a server that implements a similar email-like service.

NOTE: PLEASE MAKE SURE THAT THE MACHINES RUNNING THE SERVER AND THE CLIENT CODE BOTH ARE CONNECTED TO THE SAME NETWORK.