import socket
import threading


class ClientThread(threading.Thread):

    def __init__(self, client_ip, client_port, client_socket):
        threading.Thread.__init__(self)
        self.ip = client_ip
        self.port = client_port
        self.clientsocket = client_socket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))

    def run(self):
        r = self.clientsocket.recv(9999)

        self.clientsocket.send(("rcv: " + str(r)[2 : len(str(r)) - 1]).encode())


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
