from reading.ad_item import Ad_Item
from reading.dataset_item import Dataset_Item
import numpy as np
from typing import Dict, List

class Advertisement:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()  # type: Dict[Int, Ad_Item]
        self.dataset_create = dict()    # type: Dict[Int, List[Dataset_Item]]
        self.dataset_ad = dict()    # type: Dict[Int, List[Dataset_Item]]
        self.dataset_camgaign = dict()    # type: Dict[Int, List[Dataset_Item]]
        self.dataset_advertiser = dict()    # type: Dict[Int, List[Dataset_Item]]
        self.dataset_app = dict()    # type: Dict[Int, List[Dataset_Item]]

        self.creat_count = dict()
        self.ad_count = dict()
        self.camgaign_count = dict()
        self.advertiser_count = dict()
        self.app_count = dict()
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            creativeID, adID, camgaignID, advertiserID, appID, appPlatform = tmp
            self.data[creativeID] = Ad_Item(creativeID, adID, camgaignID, advertiserID, appID, appPlatform)
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record : Dataset_Item):
        creativeID = record.creativeID
        adID = self.data[creativeID].adID
        camgaignID = self.data[creativeID].camgaignID
        advertiserID = self.data[creativeID].advertiserID
        appID = self.data[creativeID].appID
        _day = record.clickTime // 10000
        label = record.label
        label = max(0, label)
        if creativeID not in self.dataset_create:
            self.dataset_create[creativeID] = list()
            self.creat_count[creativeID] = np.zeros([2, 32])
        if adID not in self.dataset_ad:
            self.dataset_ad[adID] = list()
            self.ad_count[adID] = np.zeros([2, 32])
        if camgaignID not in self.dataset_camgaign:
            self.dataset_camgaign[camgaignID] = list()
            self.camgaign_count[camgaignID] = np.zeros([2, 32])
        if advertiserID not in self.dataset_advertiser:
            self.dataset_advertiser[advertiserID] = list()
            self.advertiser_count[advertiserID] = np.zeros([2, 32])
        if appID not in self.dataset_app:
            self.dataset_app[appID] = list()
            self.app_count[appID] = np.zeros([2, 32])
        self.dataset_create[creativeID].append(record)
        self.dataset_ad[adID].append(record)
        self.dataset_camgaign[camgaignID].append(record)
        self.dataset_advertiser[advertiserID].append(record)
        self.dataset_app[appID].append(record)

        self.creat_count[creativeID][label][_day] += 1
        self.ad_count[adID][label][_day] += 1
        self.camgaign_count[camgaignID][label][_day] += 1
        self.advertiser_count[advertiserID][label][_day] += 1
        self.app_count[appID][label][_day] += 1

    def fresh(self):
        def push(f):
            for i in range(len(f)):
                for j in range(1, len(f[i])):
                    f[i][j] += f[i][j-1]

        for k in self.creat_count:
            push(self.creat_count[k])
        for k in self.ad_count:
            push(self.ad_count[k])
        for k in self.camgaign_count:
            push(self.camgaign_count[k])
        for k in self.advertiser_count:
            push(self.advertiser_count[k])
        for k in self.app_count:
            push(self.app_count[k])

    def get_dataset_create(self, creativeID):
        return self.dataset_create[creativeID]

    def get_dataset_ad(self, adID):
        return self.dataset_ad[adID]

    def get_dataset_camgaign(self, camgaignID):
        return self.dataset_camgaign[camgaignID]

    def get_dataset_advertiser(self, advertiserID):
        return self.dataset_advertiser[advertiserID]

    def get_dataset_app(self, appID):
        return self.dataset_app[appID]

    def get_create_count(self, creativeID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.creat_count[creativeID][:, end_t - 1] - self.creat_count[creativeID][:, from_t - 1])
        return self.creat_count[creativeID][label, end_t - 1] - self.creat_count[creativeID][label, from_t - 1]

    def get_ad_count(self, adID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.ad_count[adID][:, end_t - 1] - self.ad_count[adID][:, from_t - 1])
        return self.ad_count[adID][label, end_t - 1] - self.ad_count[adID][label, from_t - 1]

    def get_camgaign_count(self, camgaignID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.camgaign_count[camgaignID][:, end_t - 1] - self.camgaign_count[camgaignID][:, from_t - 1])
        return self.camgaign_count[camgaignID][label, end_t - 1] - self.camgaign_count[camgaignID][label, from_t - 1]

    def get_advertiser_count(self, advertiserID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.advertiser_count[advertiserID][:, end_t - 1] - self.advertiser_count[advertiserID][:, from_t - 1])
        return self.advertiser_count[advertiserID][label, end_t - 1] - self.advertiser_count[advertiserID][label, from_t - 1]

    def get_app_count(self, appID, label, from_t, end_t):
        if label == -1:
            return np.sum(self.app_count[appID][:, end_t - 1] - self.app_count[appID][:, from_t - 1])
        return self.app_count[appID][label, end_t - 1] - self.app_count[appID][label, from_t - 1]

