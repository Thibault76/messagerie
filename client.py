import socket


def byte_to_string(byte):
    return str(byte)[2: len(str(byte)) - 1]


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = 0

    def connect(self, user_id):
        self.s.connect(("localhost", 1111))
        self.send_message("id:" + str(user_id))
        self.id = user_id

    def send_message(self, msg):
        self.s.send(msg.encode())
        verification = self.receive_msg(3)
        if byte_to_string(verification) != "rcv":
            print("Error")

    def receive_msg(self, size):
        r = self.s.recv(size)
        return r

    def quit(self):
        self.send_message("quit")

    def get_username_of(self, user_id):
        self.send_message("get username of: " + str(user_id))
        return byte_to_string(self.receive_msg(100))

    def get_username(self):
        self.send_message("get username:")
        return byte_to_string(self.receive_msg(100))

    def get_message_with(self, target_id, number):
        self.send_message("get message with: " + str(target_id) + "| " + str(number))
        return byte_to_string(self.receive_msg(9999))

    def send_message_to(self, target_id, message):
        self.send_message("send message to: " + str(target_id) + "|__BY__" + str(self.id) + "__ " + message)

    def get_contacts(self):
        self.send_message("get contacts:")
        return byte_to_string(self.receive_msg(9999)).split(":")

    def add_contact(self, user_id):
        self.send_message("add contact: " + str(user_id))

