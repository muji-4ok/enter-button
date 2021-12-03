import socket
SIZE = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (input(), 8889)
sock.connect(server_address)

try:
    sock.sendall(input().encode())
    while True:
        data = sock.recv(SIZE).decode()
        if data is not None:
            print(data)
            sock.sendall(input().encode)
finally:
    sock.close()
