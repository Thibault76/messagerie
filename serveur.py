import socket
import threading


def byte_to_string(byte):
    return str(byte)[2: len(str(byte)) - 1]


class ClientThread(threading.Thread):

    def __init__(self, client_ip, client_port, client_socket):
        threading.Thread.__init__(self)
        self.ip = client_ip
        self.port = client_port
        self.clientsocket = client_socket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))
        self.client_id = 0

    def run(self):
        r = self.receive_msg(9999)

        if byte_to_string(r)[0:3] == "id:":
            self.client_id = byte_to_string(r)[3: len(byte_to_string(r))]
            run = True
            while run:
                r = self.receive_msg(9999)

                if byte_to_string(r) == "quit":
                    run = False
                    print("Client disconnected")
                else:
                    if byte_to_string(r) == "get last message rcv: ":
                        pass

                    elif byte_to_string(r) == "get last message sent":
                        pass

                    elif byte_to_string(r)[0:17] == "get username of: ":
                        user_id = byte_to_string(r)[17: len(byte_to_string(r))]
                        user_name = data[user_id]["pseudonym"]
                        self.clientsocket.send(user_name.encode())

                    elif byte_to_string(r) == "get username:":
                        user_name = data[self.client_id]["pseudonym"]
                        self.clientsocket.send(user_name.encode())

                    elif byte_to_string(r)[0: 18] == "get message with: ":
                        target_id = ""
                        i = 18
                        while byte_to_string(r)[i] != "|":
                            target_id = target_id + byte_to_string(r)[i]
                            i += 1
                        message_number = byte_to_string(r)[i + 1: len(byte_to_string(r))]
                        if int(target_id) > int(self.client_id):
                            self.clientsocket.send(discussion[self.client_id + "|" + target_id][-int(message_number)].encode())
                        else:
                            self.clientsocket.send(
                                discussion[target_id + "|" + self.client_id][-int(message_number)].encode())
        else:
            print("Error: No id")

    def receive_msg(self, size):
        r = self.clientsocket.recv(size)
        self.clientsocket.send("rcv".encode())
        return r


data = {
    "0": {
        "pseudonym": "Thibault",
        "friend whith": [1, 2]
    },
    "1": {
        "pseudonym": "Alexis",
        "friend whith": [0, 2, 3]
    },
    "2": {
        "pseudonym": "Melissa",
        "friend whith": [1, 0]
    },
    "3": {
        "pseudonym": "Papa",
        "friend whith": [4, 1]
    },
    "4": {
        "pseudonym": "Maman",
        "friend whith": [3]
    }
}

discussion = {
    "0|1": [
            "__OF__0__ Salut", "__OF__1__Salut, tu fais quoi de beau ?",
            "__OF__1__ Je mange des pates et toi ?"
        ],
    "3|4": [
        "__OF__4__ T'as pensé à sortir les  poubelles ?",
        "__OF__3__ Non, j'ai oublie...",
        "__OF__4__ Pff... Il,faut vraiment que je pense à tous dans cette famille"
    ]
}

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
