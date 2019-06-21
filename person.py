import pickle
import re
import hashlib
import random
from string import printable


LEGAL_USR_ID = """User id requirements
- a minimal length of 1
- a maximum length of 16
- characters can only be
    · a digit
    · a letter
    · a underscore
"""
USR_ID_PATTERN = r"^[\d\w_]{1,16}$"

LEGAL_PSW = """Password requirements for your data security
- a minimal length of 8
- a maximum length of 100
- at least one of each of
    · digits
    · lower case letters
    · upper case letters
"""
PSW_PATTERN = r"^[\d]*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$"

PERSON_SAVE = "save/person_details.p"


class Person:

    single = None

    def __init__(self, usr_id, password):
        self.usr_id = usr_id
        self.password = password
        self.hash = None
        self.__class__.single = self

    def register(self):

        # check usr_id and password syntax, return error message if illegal
        if not re.match(USR_ID_PATTERN, self.usr_id):
            return LEGAL_USR_ID
        if not re.match(PSW_PATTERN, self.password):
            return LEGAL_PSW

        # check if user name is registered
        try:
            # load file first
            usr_map = pickle.load(open(PERSON_SAVE, 'br'))
        except FileNotFoundError:
            usr_map = {}
        if self.usr_id in usr_map:
            return "User name is occupied"

        # generate hash
        salt = "energymax"
        pepper = random.choice(printable)
        code = self.password + salt + pepper  # add salt and pepper for better encryption
        code = code.encode("utf-8")
        self.hash = hashlib.sha256(code).hexdigest()

        # save hash
        usr_map[self.usr_id] = self.hash
        pickle.dump(usr_map, open(PERSON_SAVE, 'bw'))

    def login(self):

        # load from file
        try:
            usr_map = pickle.load(open(PERSON_SAVE, 'br'))
        except FileNotFoundError:
            return "No user registered"
        usr_hash = usr_map.get(self.usr_id)

        # check user id
        if not self.usr_id:
            return "User name cannot be empty"
        if not usr_hash:
            return "No user named " + self.usr_id + " found"

        # check password
        salt = "energymax"
        for pepper in printable:
            code = self.password + salt + pepper
            code = code.encode("utf-8")
            if usr_hash == hashlib.sha256(code).hexdigest():
                return None
        return "Incorrect password"
