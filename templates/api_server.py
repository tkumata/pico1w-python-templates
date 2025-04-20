import socket
import time

import network

# Wi-Fi Station
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')
while not wlan.isconnected():
    time.sleep(1)
print('Connected to Wi-Fi')
print('IP Address:', wlan.ifconfig()[0])
print('Network Mask:', wlan.ifconfig()[1])
print('Gateway:', wlan.ifconfig()[2])
print('DNS Server:', wlan.ifconfig()[3])


# HTTP Server
def handle_request(client_socket):
    request = client_socket.recv(1024)
    print('Received request:')
    print(request)

    try:
        request_line = request.decode().split('\r\n')[0]
        method, path, _ = request_line.split()

        if path == '/':
            response_body = '{"response": "Root path"}'
        elif path == '/hello':
            response_body = '{"response": "Hello from MicroPython!"}'
        elif path == '/status':
            response_body = '{"status": "ok"}'
        else:
            response_body = 'Not Found'
            response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n{response_body}'
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        content_type = 'application/json'
        response = (
            f'HTTP/1.1 200 OK\r\n'
            f'Content-Type: {content_type}\r\n'
            f'Content-Length: {len(response_body)}\r\n'
            f'\r\n'
            f'{response_body}'
        )
        client_socket.sendall(response.encode())
    except Exception as e:
        error_response = 'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError'
        client_socket.sendall(error_response.encode())
        print('Error:', e)
    finally:
        client_socket.close()


# HTTP Socket (TCP)
http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http_socket.bind(('0.0.0.0', 80))
http_socket.listen(5)
http_socket.setblocking(False)

while True:
    try:
        client_socket, addr = http_socket.accept()
        print('Accepted connection from:', addr)
        handle_request(client_socket)
    except OSError:
        pass
    time.sleep(0.01)
