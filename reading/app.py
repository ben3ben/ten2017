from reading.app_item import App_Item
from reading.dataset_item import Dataset_Item
from typing import Dict, List

class App:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()  # type: Dict[Int, App_Item]
        self.dataset_app_cat = dict()   # type: Dict[Int, List[Dataset_Item]]
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            appID, appCategory = tmp
            self.data[appID] = App_Item(appID, appCategory)
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record : Dataset_Item, appCategory):
        if appCategory not in self.dataset_app_cat:
            self.dataset_app_cat[appCategory] = list()
        self.dataset_app_cat[appCategory].append(record)

    def get_dataset(self, appCategory):
        return self.dataset_app_cat[appCategory]