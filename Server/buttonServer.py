import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()

    try:
            print (sys.stderr, 'connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(9000)
                print (sys.stderr, 'received "%s"' % data.decode())
                # wait for "See Server Mappings" button to be pressed to retransmit data
                if "return" in data.decode():
                    connection.sendall(data)
                    print(sys.stderr, 'sending data back to the client')
                # if data:
                    # print (sys.stderr, 'sending data back to the client')
                    # connection.sendall(data)
                # else:
                if not data:
                    print (sys.stderr, 'no more data from', client_address)
                    break

    finally:
        # Clean up the connection
        connection.close()