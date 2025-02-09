from socket import socket, AF_INET, SOCK_STREAM
from json import loads, dumps


HOST_IP = 'localhost'
HOST_PORT = 12000
END_MARK = '\0'


data_list = []


def dict_to_json(func) -> str:
    def wrapper(*args, **kwargs) -> str:
        return dumps(func(*args, **kwargs))
    
    return wrapper

@dict_to_json
def handle(request: str) -> dict:
    try:
        request: dict = loads(request)

    except ValueError:
        return  {'code': 422, 'message': 'Unprocessable Entity', 'data': None}

    method = request.get('method')
    path = request.get('path')
    data = request.get('data')

    if method == 'GET':
        if path == '/':
            return {'code': 200, 'message': 'OK', 'data': 'Hello, World!'}

        if path == '/echo':
            return {'code': 200, 'message': 'OK', 'data': data}

        if path == '/list':
            return {'code': 200, 'message': 'OK', 'data': data_list}

        else:
            return {'code': 400, 'message': 'Bad Request', 'data': None}
        
    elif method == 'POST':
        if path == '/item':
            data_list.append(data)

            return {'code': 201, 'message': 'Created', 'data': None}

        else:
            return {'code': 400, 'message': 'Bad Request', 'data': None}
        
    elif method == 'PUT':
        if path == '/item':
            try:
                current, new = data.split(',')
                index = data_list.index(current)
                data_list[index] = new

            except ValueError:
                return {'code': 404, 'message': 'Not Found', 'data': None}

            return {'code': 200, 'message': 'OK', 'data': None}

        else:
            return {'code': 400, 'message': 'Bad Request', 'data': None}
        
    elif method == 'DELETE':
        if path == '/item':
            try:
                data_list.remove(data)
            except ValueError:
                return {'code': 404, 'message': 'Not Found', 'data': None}

            return {'code': 204, 'message': 'No Content', 'data': None}  # Processed successfully, but no content to return

        else:
            return {'code': 400, 'message': 'Bad Request', 'data': None}

    else:
        return {'code': 400, 'message': 'Bad Request', 'data': None}

def run_server():
    server = socket(AF_INET, SOCK_STREAM)  # Create a socket object
    server.bind((HOST_IP, HOST_PORT))  # Make the socket listen to the specified port

    server.listen(1)  # Enable the server to accept connections
    print(f'Server is listening on {HOST_IP}:{HOST_PORT}')

    while True:
        conn, addr = server.accept()  # Accept a connection
        buffer = ''  # Initialize a buffer to store the received data

        while True:
            data = conn.recv(1024)  # Receive data from the client
            buffer += data.decode('utf-8')  # Decode the received data and add it to the buffer

            has_closed_request = buffer[-1] == END_MARK  # Check if the buffer contains a closed request

            if has_closed_request:
                request = buffer[:-1]  # Extract the request from the buffer
                print(f'Request from {addr}: {request}')

                response = handle(request)  # Handle the request

                # Send the received data back to the client
                conn.sendall(response.encode('utf-8'))
                conn.close()

                break
