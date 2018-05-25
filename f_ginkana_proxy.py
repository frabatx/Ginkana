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

        socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketserver.bind(('', tcp_port))
        socketserver.listen(30)

        t = threading.Thread(target=tcp_server, args=(socketserver,))
        t.setDaemon(True)
        t.start()

        socketproxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketproxy.connect((uclm_url, uclm_port))

        message = "{} {}".format(code, tcp_port)

        socketproxy.send(message.encode())

        msg, client = socketproxy.recvfrom(1024)

        print(msg.decode())

        socketserver.close()
        socketproxy.close()


def tcp_server(socketserver):

    while True:
        clientsocket, client = socketserver.accept()
        t = threading.Thread(target=download_and_send_webpage, args=(clientsocket,))
        t.start()


def download_and_send_webpage(clientsock):

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