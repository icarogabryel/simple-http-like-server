from socket import socket, AF_INET, SOCK_STREAM


HOST_IP = 'localhost'
HOST_PORT = 12000

END_MARK = '\0'


def request_handler(request):
    return '200'

def run():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST_IP, HOST_PORT))

    server.listen(1)
    print(f'Server is listening on {HOST_IP}:{HOST_PORT}')

    while True:
        conn, addr = server.accept()  # Accept a connection
        buffer = ''  # Initialize a buffer to store the received data

        while True:
            data = conn.recv(1024)  # Receive data from the client
            buffer += data.decode('utf-8')  # Decode the received data and add it to the buffer

            has_closed_request = buffer[-1] == END_MARK  # Check if the buffer contains a closed request

            if has_closed_request:
                request = buffer
                print(f'Request from {addr}: {request}')

                response = request_handler(request)  # Handle the request

                # Send the received data back to the client
                conn.sendall(response.encode('utf-8'))
                conn.close()

                break
