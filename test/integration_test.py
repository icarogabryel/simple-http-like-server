# Integration test: send a message to the server

from socket import socket, AF_INET, SOCK_STREAM


HOST_IP = 'localhost'
HOST_PORT = 12000

END_MARK = '\0'


def send_message(message):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST_IP, HOST_PORT))

    client.sendall(message.encode('utf-8'))

    response = client.recv(1024)
    print(f'response: {response.decode('utf-8')}')


if __name__ == '__main__':
    while True:
        message = input('Enter a message: ') + END_MARK
        send_message(message)
