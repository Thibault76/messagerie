class Xml:
    def __init__(self, file_open):
        self.file = open(file_open, "r+")
        self.brut_data = ""
        self.clear_data = {}
        self.i = 0

    def close(self):
        self.file.close()

    def read(self):
        self.brut_data = self.file.read()

        run = True
        self.i = 0
        self.clear_data = self.read_xml_info()

        while run:
            self.move_to_next("<", 0)
            if self.is_exceeded():
                run = False
            else:
                data = self.read_tag()
                for key, value in data.items():
                    self.clear_data[key] = value

            self.i += 1

    def read_tag(self):
        data = {}

        if not self.is_exceeded():
            self.move_to_next("<", 1)
            if not self.brut_data[self.i] == "/":
                name_of_tag = self.read_name_tag()
                if name_of_tag != "!--":
                    data[name_of_tag] = {"arguments": {}, "child": {}}
                    while self.brut_data[self.i] == " ":
                        self.i += 1
                    if self.brut_data[self.i] == "/":
                        data[name_of_tag]["arguments"] = {}
                    else:
                        self.i -= 1
                        data[name_of_tag]["arguments"] = self.read_arg()
                        if self.brut_data[self.i] == "/" and self.brut_data[self.i + 1] == ">":
                            data[name_of_tag]["child"] = {}
                        else:
                            self.move_to_next("<", 1)
                            if self.read_name_tag() == "/" + name_of_tag:
                                data[name_of_tag]["child"] = {}
                            else:
                                self.move_to_back("<", 1)
                                data[name_of_tag]["child"] = self.read_tag()
                else:
                    self.skip_comment()

        return data

    def read_name_tag(self):
        name_of_tag = ""
        while self.brut_data[self.i] != " " and self.brut_data[self.i] != ">":
            name_of_tag = name_of_tag + self.brut_data[self.i]
            self.i += 1
        return name_of_tag

    def read_arg(self):
        a = {}
        run = True
        while run:
            name_arg = ""
            arg_value = ""
            self.i += 1

            if self.is_exceeded() or self.brut_data[self.i] == "/":
                run = False
            else:
                while self.brut_data[self.i] != "=":
                    name_arg = name_arg + self.brut_data[self.i]
                    self.i += 1
                self.move_to_next("\"", 1)
                while self.brut_data[self.i] != "\"":
                    arg_value = arg_value + self.brut_data[self.i]
                    self.i += 1
                a[name_arg] = arg_value

                self.i += 1

                while self.brut_data[self.i] == " ":
                    self.i += 1

                if self.brut_data[self.i] == ">" or self.brut_data[self.i] == "/" or self.brut_data[self.i] == "?":
                    run = False
                else:
                    self.i -= 1
        return a

    def get_data(self):
        return self.clear_data

    def move_to_next(self, letter, add):
        if not self.is_exceeded():
            while self.brut_data[self.i] != letter and not self.is_exceeded():
                self.i = self.i + 1
            self.i += add

    def move_to_back(self, letter, rem):
        while self.brut_data[self.i] != letter:
            self.i = self.i - 1
        self.i -= rem

    def is_exceeded(self):
        if self.i >= (len(self.brut_data) - 1):
            return True
        else:
            return False

    def read_xml_info(self):
        data = {}
        self.move_to_next("<", 1)
        tag = self.read_name_tag()
        if tag == "?xml":
            data["info"] = self.read_arg()

        print(self.brut_data[self.i])
        self.i += 1

        return data

    def skip_comment(self):
        self.move_to_next("-", 0)
        tag = self.brut_data[self.i] + self.brut_data[self.i + 1]
        while tag != "->":
            self.move_to_next("-", 1)
            tag = self.brut_data[self.i] + self.brut_data[self.i + 1]

file = Xml("xml.xml")
file.read()
print(file.get_data())
file.close()
