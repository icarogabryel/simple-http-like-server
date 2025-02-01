# Load test: send a large message to the server to see if the buffer is working correctly

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
        input('Press enter to do the test.')
        send_message(('a' * 10000) + END_MARK)
