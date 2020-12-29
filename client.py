import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1111))

print("Le nom du fichier que vous voulez récupérer:")
file_name = input(">> ")
s.send(file_name.encode())
file_name = 'data/%s' % (file_name, )
r = s.recv(9999999)
with open(file_name,'wb') as _file:
    _file.write(r)
print("Le fichier a été correctement copié dans : %s." % file_name)
