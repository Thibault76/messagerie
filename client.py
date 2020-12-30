import socket

"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.2", 1111))

print("Le nom du fichier que vous voulez récupérer:")
file_name = input(">> ")
s.send(file_name.encode())
file_name = 'data/%s' % (file_name, )
r = s.recv(9999999)
with open(file_name,'wb') as _file:
    _file.write(r)
print("Le fichier a été correctement copié dans : %s." % file_name)
"""


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

me = Client()
me.connect(3)
print(me.get_username())
print(me.get_message_with(4, 1))
me.quit()
