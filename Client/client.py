import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
host = "10.145.103.233"
server_address = (host, 10000)
print (sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)


try:
    # Send data
    filename="UT_Austin_Wafermap1.txt"
    f = open(filename,'rb')
    amount_expected =0;
    while True:
        message = f.read(1024)
        if not message:
            break
        # message = "This is the message.  It will be repeated."
        print (sys.stderr, 'sending "%s"\n' % message)
        # sock.sendall(message)
        sock.sendto(message,server_address)
        # Look for the response
        amount_received = 0

        amount_expected = len(message)

        # while amount_received < amount_expected:
        #     data = sock.recv(1024)
        #     amount_received += len(data)
        #     print (sys.stderr, 'received "%s"\n' % data.decode())

finally:
    print (sys.stderr, 'closing socket')
    sock.close()
