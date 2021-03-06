from reading.user_app_action_item import User_App_Action_Item
from typing import Dict, List

class User_App_Actions:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()  # type: Dict[Int, List[User_App_Action_Item]]
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            userID, installTime, appID = tmp
            if userID not in self.data:
                self.data[userID] = list()
            d = User_App_Action_Item(userID, installTime, appID)
            self.data[userID].append(d)
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        if key not in self.data:
            return list()
        return self.data[key]

    def exists(self, key):
        return key in self.data
