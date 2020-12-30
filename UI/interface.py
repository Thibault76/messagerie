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

        # connection
        self.connectionMenu = tk.Frame(self.tk, bg="#31bffd")
        self.idEntry = tk.Entry(self.connectionMenu, width=75, bd=0, bg="#ffffff", relief="flat")
        self.idEntry.pack()
        self.connectButton = tk.Button(self.connectionMenu, text="connect", bd=0, command=self.connect)
        self.connectButton.pack(pady=25)

        # contacts
        self.contacts = tk.Frame(self.tk, bg="#31bffd", width=1080, height=720)
        self.contacts.pack_propagate(False)
        self.contactList = tk.Listbox(self.contacts, relief="flat", width=60, height=1000)
        self.contactList.pack(side="right")

        self.set_window('connection')

    def set_window_attributes(self, title="messagerie", size="1080x720"):
        self.tk.title(title)
        self.tk.geometry(size)

    def set_window(self, window):
        if window == 'connection':
            self.tk.config(background="#31bffd")
            self.connectionMenu.pack(expand="YES")

        elif window == "contacts":
            self.connectionMenu.pack_forget()
            self.contacts.pack(expand='YES')

            self.get_contacts()

    def get_contacts(self):
        contacts = self.user.get_contacts()

        for i in range(0, len(contacts)):
            self.contactList.insert(str(i), self.user.get_username_of(int(contacts[i])))

    def get_contact_info(self, user_id):
        pass

    def get_friends(self):
        pass

    def send_to(self, user_id):
        pass

    def get_from(self, user_id):
        pass

    def run(self):
        self.tk.mainloop()

    def disconnect(self):
        self.user.quit()

    def connect(self):
        try:
            self.user_id = int(self.idEntry.get())

        except ValueError:
            ERR("interface.connect", "cannot load an int from a str value")
            return False

        self.user.connect(self.user_id)
        self.set_window("contacts")
