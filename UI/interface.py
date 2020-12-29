import tkinter
import xml

class Inerface:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.path = None

    def reload(self):
        xml = xml.Xml(self.path)


