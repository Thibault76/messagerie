import socket
import threading


def byte_to_string(byte):
    return str(byte)[2: len(str(byte)) - 1]


class ClientThread(threading.Thread):
    def __init__(self, client_ip, client_port, client_socket_data):
        threading.Thread.__init__(self)
        self.ip = client_ip
        self.port = client_port
        self.client_socket = client_socket_data
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))
        self.client_id = 0
        self.current_msg_rcv = ""

    def get_username_of(self):
        user_id = self.current_msg_rcv[17: len(self.current_msg_rcv)]
        user_name = data[user_id]["pseudonym"]
        self.client_socket.send(user_name.encode())

    def get_username(self):
        user_name = data[str(self.client_id)]["pseudonym"]
        self.client_socket.send(user_name.encode())

    def get_msg(self):
        target_id = ""
        i = 18
        while self.current_msg_rcv[i] != "|":
            target_id = target_id + self.current_msg_rcv[i]
            i += 1
        message_number = self.current_msg_rcv[i + 1: len(self.current_msg_rcv)]
        if int(target_id) > int(self.client_id):
            self.client_socket.send(
                discussion[str(self.client_id) + "|" + target_id][-int(message_number)].encode())
        else:
            self.client_socket.send(
                discussion[target_id + "|" + str(self.client_id)][-int(message_number)].encode())

    def send_message_to(self):
        i = 17
        target_id = ""
        while self.current_msg_rcv[i] != "|":
            target_id = target_id + self.current_msg_rcv[i]
            i += 1
        i += 1
        message = self.current_msg_rcv[i: len(self.current_msg_rcv)]

        if int(target_id) > int(self.client_id):
            name_key = str(self.client_id) + "|" + str(target_id)
        else:
            name_key = str(target_id) + "|" + str(self.client_id)

        if name_key in discussion:
            discussion[name_key].append(message)
        else:
            discussion[name_key] = [message]

        print(discussion)

    def get_contact(self):
        list_contacts = data[str(self.client_id)]["friend with"]
        string_contacts = ":".join(list_contacts)
        self.send_message(string_contacts)

    def add_contact(self):
        user_id = self.current_msg_rcv[13: len(self.current_msg_rcv)]
        if data[str(self.client_id)]["friend with"].count(user_id) == 0:
            data[str(self.client_id)]["friend with"].append(user_id)

    def run(self):
        r = self.receive_msg(9999)

        if byte_to_string(r)[0:3] == "id:":
            self.client_id = byte_to_string(r)[3: len(byte_to_string(r))]
            run = True
            while run:

                self.current_msg_rcv = byte_to_string(self.receive_msg(9999))

                if self.current_msg_rcv == "quit":
                    run = False
                    print("Client disconnected")
                else:
                    if self.current_msg_rcv[0:17] == "get username of: ":
                        self.get_username_of()
                    elif self.current_msg_rcv == "get username:":
                        self.get_username()
                    elif self.current_msg_rcv[0: 18] == "get message with: ":
                        self.get_msg()
                    elif self.current_msg_rcv[0: 17] == "send message to: ":
                        self.send_message_to()
                    elif self.current_msg_rcv == "get contacts:":
                        self.get_contact()
                    elif self.current_msg_rcv[0: 13] == "add contact: ":
                        self.add_contact()
        else:
            print("Error: No id")

    def receive_msg(self, size):
        r = self.client_socket.recv(size)
        self.client_socket.send("rcv".encode())
        return r

    def send_message(self, message):
        self.client_socket.send(message.encode())


data = {
    "0": {
        "pseudonym": "Thibault",
        "friend with": ["1", "2"]
    },
    "1": {
        "pseudonym": "Alexis",
        "friend with": ["0", "2", "3"]
    },
    "2": {
        "pseudonym": "Melissa",
        "friend with": ["1", "0"]
    },
    "3": {
        "pseudonym": "Papa",
        "friend with": ["4", "1"]
    },
    "4": {
        "pseudonym": "Maman",
        "friend with": ["3"]
    }
}

discussion = {
    "0|1": [
            "__BY__0__ Salut", "__OF__1__Salut, tu fais quoi de beau ?",
            "__BY__1__ Je mange des pates et toi ?"
        ],
    "3|4": [
        "__BY__4__ T'as pensé à sortir les  poubelles ?",
        "__BY__3__ Non, j'ai oublie...",
        "__BY__4__ Pff... Il faut vraiment que je pense a tous dans cette famille"
    ]
}

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (client_socket, (ip, port)) = tcpsock.accept()
    new_thread = ClientThread(ip, port, client_socket)
    new_thread.start()
