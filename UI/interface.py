from log import *
from UI import contact
import client as cl
import tkinter as tk


class Interface:
    def __init__(self):

        self.tk = tk.Tk()
        self.set_window_attributes()

        self.user_id = 0

        self.user = cl.Client()

        self.connectionMenu = tk.Frame(self.tk, width=1080, height=720, bg="#31bffd")
        self.idEntry = tk.Entry(self.connectionMenu, width=75, bd=0, bg="#ffffff", relief="flat")
        self.idEntry.pack()

        self.connectButton = tk.Button(self.connectionMenu, text="connect", bd=0, command=self.connect())
        self.connectButton.pack(pady=25)

        self.set_window('connection')

    def set_window_attributes(self, title="messagerie", size="1080x720"):
        self.tk.title(title)
        self.tk.geometry(size)

    def set_window(self, window):
        if window == 'connection':
            self.tk.config(background="#31bffd")
            self.connectionMenu.pack(expand="YES")

    def get_contacts(self):
        pass

    def get_contact_info(self, user_id):
        pass

    def get_friends(self):
        pass

    def send_to(self, user_id):
        pass

    def get_from(self, user_id):
        pass

    def write(self):
        pass

    def run(self):
        self.tk.mainloop()

    def deconnect(self):
        self.user.quit()

    def connect(self):
        try:
            print(self.idEntry.get())

        except ValueError:
            ERR("interface.connect", "cannot load an int from a str value")
            return False


        #self.user.connect(self.user_id)

