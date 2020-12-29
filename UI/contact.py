from log import *

class Contact:
    def __init__(self, user_id, username="userName"):
        self.userName = username
        self.id = user_id

        LOG("adding {} : {} to contacts".format(username, user_id))