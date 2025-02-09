# Simple HTTP-Like Server

In this repo, You will find a simple HTTP-like server written in Python. The server is build over TCP sockets and uses a minimalistic version of the HTTP protocol.

## The Protocol

Just like the HTTP protocol, the server uses a request-response model. Both requests and responses are JSON objects.

<div style="display: flex; justify-content: center; width: 100%;">
    <div style="flex: 1; margin-right: 10px;">
        <h3>Requests</h3>
        <p>The requests have the following fields:</p>
        <ul>
            <li><code>method</code>: The HTTP method used in the request. They can be GET, POST, PUT and DELETE.</li>
            <li><code>path</code>: The path of the requested resource.</li>
            <li><code>data</code>: The data sent in the request body.</li>
        </ul>
    </div>
    <div style="flex: 1;">
        <h3>Responses</h3>
        <p>The responses have the following fields:</p>
        <ul>
            <li><code>code</code>: The status code of the response.</li>
            <li><code>message</code>: The status message of the response.</li>
            <li><code>data</code>: The data sent in the response body.</li>
        </ul>
    </div>
</div>

## How It Works

1. Server Reception:

    This server uses a TCP socket and listens for incoming connections. When a connection is received, the server reads the incoming data and put it into a buffer. Every received data is added to this buffer until the end marker `\0` is found. After the end marker is found, the server processes the request. Because the server is stateless, it closes the connection after sending the response.

2. Request Handling:

    The server parses the received data into a JSON object in the `handle` function. Then, it checks if the request is valid. If the request is valid, the server processes it and sends a response. If the request is invalid, the server sends an error response.

3. Response Sending:

    The server sends the response to the client. The response is sent as a JSON object. The server sends the response in the following format:

    ```json
    {
        "code": 200,
        "message": "OK",
        "data": "Hello, World!"
    }
    ```

## Tests

The server was tested using the files in the `tests` folder. It was made integration tests, load tests and function tests. This last one is the principal and was made using a series of `assert` statements like below:

```python
    response = send_message(dumps({'method': 'GET', 'path': '/'}))
    assert response == dumps({'code': 200, 'message': 'OK', 'data': 'Hello, World!'})
```

## How to Run

To run the server, you need to have Python installed on your machine. You can run the server by executing the `main.py` file in the `src` folder following command in your terminal:

```bash
python main.py
```
