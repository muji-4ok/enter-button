import socket
SIZE = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8889)
sock.bind(server_address)

sock.listen()

while True:
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(SIZE).decode()
            if data is not None:
                print(data)
                connection.sendall(input().encode())
    finally:
        connection.close()
