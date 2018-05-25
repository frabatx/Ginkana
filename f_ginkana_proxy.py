'''
Step 5: Proxy Web
------------------

- Create an HTTP Proxy server on your computer (in the port of your choice).
- Your server will receive a random amount of HTTP requests for download
  third-party URLs, you must download these resources (using HTTP) and
  return them to the requesting customer.

 +--------+        +--------------+       +-------------+
 | Client |        | Proxy server |       | HTTP server |
 +--------+        +--------------+       +-------------+
      |                    |                     |
      |  GET(server, url)  |                     |
      +------------------>+++  connect(server)   |
      |                   | |------------------->|
      |                   | |   file: GET(url)   |
      |      file         | |------------------->|
      |<------------------+++                    |
      |                    |                     |


- Create a client socket and send a message to the server TCP atclab.esi.uclm.es:9000
  Indicating the identifier "42744" and the port on which you have created
  Your proxy server, separated by a space.
  Example: "42744 7777".
- Through the same socket you will receive further instructions or information
  about errors.

Hints:
- Caution: Your proxy will receive simultaneous requests and it is expected that
  serve them quickly. If it takes too long, this step will fail. In order to
  achieve it create a concurrent server for your proxy.
- You can prove that your proxy is right by executing it as a independent program
  (unrelated to ginkana) and configuring your browser to use it.

Restrictions:
- It is not allowed to use the classes HTTPServer,
  SimpleHTTPServer.SimpleHTTPRequestHandler and the http.server module.

You have 5 seconds.

'''

import socket
import threading
from urllib.request import urlopen, Request

uclm_url = "atclab.esi.uclm.es"
uclm_port = 9000
tcp_port = 11111

class Step5():

    def __init__(self):
        super().__init__()

    def run(self, code):
        print("------------STEP5------------")

        # Creating socket server
        socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.bind(('', tcp_port))
        socketserver.listen(30)
        # Creating new thread object direct on tcp server
        t = threading.Thread(target=tcp_server, args=(socketserver,))
        t.setDaemon(True)
        t.start() # Starting thread

        # Creating socket proxy
        socketproxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketproxy.connect((uclm_url, uclm_port))

        message = "{} {}".format(code, tcp_port)
        # Sending message
        socketproxy.send(message.encode())
        # Receiving message
        msg, client = socketproxy.recvfrom(1024)

        print(msg.decode())

        socketserver.close()
        socketproxy.close()

# Creating a tcp server
def tcp_server(socketserver):

    while True:
        clientsocket, client = socketserver.accept()
        t = threading.Thread(target=down_send, args=(clientsocket,))
        t.start()

# Download and send file and requests
def down_send(clientsock):

    data = clientsock.recv(1024)
    print(data.decode())

    url = data.split()[1].decode()

    print("Downloading file {}".format(url))
    url_request = Request(url)
    my_file = urlopen(url_request)
    downloaded_file = my_file.read()

    print("Sending file {}".format(url))
    clientsock.send(downloaded_file)

    clientsock.close()