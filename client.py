# Client code
import socket
import threading
import time
import ssl

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('servers_ip_here', 9999)
print('Connecting to {} port {}'.format(*server_address))

# Create an SSL context
# Create an SSL context
context = ssl.create_default_context()
#context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Wrap the socket with SSL
wrapped_socket = context.wrap_socket(client_socket, server_hostname=server_address[0])

# Connect to the server
wrapped_socket.connect(server_address)

# Flag to indicate whether to keep receiving messages
keep_receiving = True

# Variable to store the email address
email_address = None

def receive_message():
    global keep_receiving
    global email_address
    while keep_receiving:
        # Receive message from the server
        data = wrapped_socket.recv(1024).decode()
        if data.startswith('HELO '):
            # Extract the email address from the message
            email_address = data[5:]
            print('Server: Your email address is:', email_address)
        elif data.startswith('New message from '):
            print('\nSERVER SAYS', data)
            time.sleep(2)
            print("Enter a message to send to the server: ")
        else:
            print('SERVER SAYS', data)

def send_message():
    global keep_receiving
    try:
        while True:
            # Take input from the user
            time.sleep(2)
            message = input("Enter a message to send to the server: ")

            # Send the user's message to the server
            wrapped_socket.sendall(message.encode())

            if message == 'QUIT':
                print('Closing the connection')
                keep_receiving = False
                break
    finally:
        # Check if the socket is still open before trying to receive data
        # Clean up the connection
        wrapped_socket.close()

# Start new threads to handle receiving and sending messages
threading.Thread(target=receive_message).start()
threading.Thread(target=send_message).start()