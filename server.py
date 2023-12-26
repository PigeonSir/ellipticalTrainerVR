import socket
import threading

bind_ip = "192.168.178.73" # Replace this with your own IP address
bind_port = 27700 # Feel free to change this port
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Server is listening on %s:%d" % (bind_ip, bind_port))


while True:
    # wait for client to connect
    client, addr = server.accept()
    print("Client connected " + str(addr))
    # create and start a thread to handle the client
    client_handler = threading.Thread(target = clientHandler, args=(client,))
    client_handler.start()