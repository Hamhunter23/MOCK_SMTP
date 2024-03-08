# Server code
import socket
import threading
import rsa
import time
import ssl
import sys

# Generate public and private keys
(public_key, private_key) = rsa.newkeys(512)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('your_ip_here', 9999)
print('Starting up on {} port {}'.format(*server_address))

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

# SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
try:
    context.load_cert_chain(certfile=r"\certificate.pem", keyfile=r"\key.pem")
    server_socket = context.wrap_socket(server_socket, server_side=True)
    print("Socket successfully wrapped with SSL")
except ssl.SSLError as e:
    print(f"Failed to wrap socket with SSL. Error: {e}")
    sys.exit(1)

# Initialize a counter for the email addresses
email_counter = 0
email_addresses = []
connections = {}


def handle_client(connection, client_address):
    global email_counter
    global email_addresses
    global connections
    email_counter += 1
    email_address = 'user{}@example.com'.format(email_counter)
    email_addresses.append(email_address)
    connections[email_address] = connection

    try:
        print('Connection from', client_address)

        while True:
            try:
                time.sleep(2)
                # Receive data from the client
                data = connection.recv(1024).strip()
            except ConnectionAbortedError:
                print('Connection aborted by the client.')
                break
            if data == b'HELO':
                # Send the email address to the client
                connection.sendall(('HELO ' + email_address).encode())
            elif data.startswith(b'MAIL FROM: '):
                sender_address_client = data.decode()[11:]
                #print(sender_address_client)
                #print(email_address)
                if(email_address == sender_address_client):
                    connection.sendall(('250 Sender '+email_address+' OK').encode())
                    connection.sendall(b'Enter the recipient email address: ')
                else: 
                    connection.sendall(b'550 Sender address rejected :(')
            elif data.startswith(b'RCPT TO: '):
                recipient_address_client = data.decode()[9:]
                #print(recipient_address_client)

                if recipient_address_client in email_addresses:
                    connection.sendall(('250 Recipient '+recipient_address_client+' OK').encode())
                    connection.sendall(b'Enter the message: ')
                else:
                    connection.sendall(b'550 Recipient address rejected :(')
            elif data.startswith(b'DATA: '):
                message = data.decode()[6:]
                connection.sendall(b'250 Message accepted for delivery')
                #connection.sendall(('Please confirm these details:\nFROM: '+sender_address_client+'\nTO: '+recipient_address_client+'\nMESSAGE:'+message).encode())
                if recipient_address_client in connections:
                    recipient_connection = connections[recipient_address_client]
                    recipient_connection.sendall(('New message from '+sender_address_client+': '+message).encode())
            elif data == b'CANCEL':
                recipient_address_client = 'NONE'
                sender_address_client = 'NONE'
                connection.sendall(b'250, Sender and Recipient addresses cleared')
            elif data == b'RCKEY':
                # Send public key to the client
                connection.sendall(public_key.save_pkcs1())
            elif data == b'HI':
                # Send hello message to the client
                connection.sendall(b'Hello')
            elif data == b'QUIT':
                connection.sendall(b'ENDING CONNECTION, BYE BYE')
                # End the connection
                break
            else: 
                connection.sendall(b'Unknown Command')

    finally:
        # Clean up the connection
        connection.close()

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()

    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(connection, client_address)).start()