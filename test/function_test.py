# Function test: Validate the responses from the server

from socket import socket, AF_INET, SOCK_STREAM
from json import dumps


HOST_IP = 'localhost'
HOST_PORT = 12000
END_MARK = '\0'


def send_message(message: str) -> None:
    message += END_MARK

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST_IP, HOST_PORT))

    client.sendall(message.encode('utf-8'))
    response = client.recv(1024)

    return response.decode('utf-8')


if __name__ == '__main__':
    # Unprocessable Entity
    response = send_message('Hello, World!')
    assert response == dumps({'code': 422, 'message': 'Unprocessable Entity', 'data': None})

    # Test GET /
    response = send_message(dumps({'method': 'GET', 'path': '/'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': 'Hello, World!'})

    # Test GET /echo
    response = send_message(dumps({'method': 'GET', 'path': '/echo', 'data': 'Hello again!'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': 'Hello again!'})

    # Test GET /list
    response = send_message(dumps({'method': 'GET', 'path': '/list'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': []})

    # Test POST /item
    response = send_message(dumps({'method': 'POST', 'path': '/item', 'data': 'Hello_1'}))
    assert response == dumps({'code': 201, 'message': 'Created', 'data': None})

    response = send_message(dumps({'method': 'POST', 'path': '/item', 'data': 'Hello_2'}))
    assert response == dumps({'code': 201, 'message': 'Created', 'data': None})

    # POST /invalid
    response = send_message(dumps({'method': 'POST', 'path': '/invalid', 'data': 'Hello_3'}))
    assert response == dumps({'code': 400, 'message': 'Bad Request', 'data': None})

    # GET /list
    response = send_message(dumps({'method': 'GET', 'path': '/list'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': ['Hello_1', 'Hello_2']})

    # GET /invalid
    response = send_message(dumps({'method': 'GET', 'path': '/invalid'}))
    assert response == dumps({'code': 400, 'message': 'Bad Request', 'data': None})

    # Test PUT /item
    response = send_message(dumps({'method': 'PUT', 'path': '/item', 'data': 'Hello_1,Hello_4!'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': None})

    # PUT /item invalid
    response = send_message(dumps({'method': 'PUT', 'path': '/item', 'data': 'Hello_1,Hello_5!'}))
    assert response == dumps({'code': 404, 'message': 'Not Found', 'data': None})

    # PUT /invalid
    response = send_message(dumps({'method': 'PUT', 'path': '/invalid', 'data': 'Hello_1,Hello_5!'}))
    assert response == dumps({'code': 400, 'message': 'Bad Request', 'data': None})

    # DELETE /item
    response = send_message(dumps({'method': 'DELETE', 'path': '/item', 'data': 'Hello_2'}))
    assert response == dumps({'code': 204, 'message': 'No Content', 'data': None})

    # DELETE /item invalid
    response = send_message(dumps({'method': 'DELETE', 'path': '/item', 'data': 'Hello_2'}))
    assert response == dumps({'code': 404, 'message': 'Not Found', 'data': None})

    # DELETE /invalid
    response = send_message(dumps({'method': 'DELETE', 'path': '/invalid', 'data': 'Hello_2'}))
    assert response == dumps({'code': 400, 'message': 'Bad Request', 'data': None})

    # Invalid method
    response = send_message(dumps({'method': 'INVALID', 'path': '/'}))
    assert response == dumps({'code': 400, 'message': 'Bad Request', 'data': None})

    # Get final list
    response = send_message(dumps({'method': 'GET', 'path': '/list'}))
    print(response)

    print('All tests passed!')
