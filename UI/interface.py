import tkinter
import tkinter.font as tkFont
import json
from log import *
from UI import contact

class Interface:
    def __init__(self):
        LOG("init tkinter")
        self.tk = tkinter.Tk()
        self.contacts = tkinter.Listbox(bd=0, activestyle='none', width=40, height=720)

        self.tk.geometry("1080x720")
        self.tk.minsize(720, 440)

        self.contacts.pack(side="right")

    def run(self):
        self.tk.mainloop()
