class Advertisement:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()
        self.dataset_create = dict()
        self.dataset_ad = dict()
        self.dataset_camgaign = dict()
        self.dataset_advertiser = dict()
        self.dataset_app = dict()
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            creativeID, adID, camgaignID, advertiserID, appID, appPlatform = tmp
            self.data[creativeID] = {'creativeID': creativeID,
                                     'adID': adID,
                                     'camgaignID': camgaignID,
                                     'advertiserID': advertiserID,
                                     'appID': appID,
                                     'appPlatform': appPlatform }
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record):
        creativeID = record['creativeID']
        adID = self.data[creativeID]['adID']
        camgaignID = self.data[creativeID]['camgaignID']
        advertiserID = self.data[creativeID]['advertiserID']
        appID = self.data[creativeID]['appID']
        if creativeID not in self.dataset_create:
            self.dataset_create[creativeID] = list()
        if adID not in self.dataset_ad:
            self.dataset_ad[adID] = list()
        if camgaignID not in self.dataset_camgaign:
            self.dataset_camgaign[camgaignID] = list()
        if advertiserID not in self.dataset_advertiser:
            self.dataset_advertiser[advertiserID] = list()
        if appID not in self.dataset_app:
            self.dataset_app[appID] = list()
        self.dataset_create[creativeID].append(record)
        self.dataset_ad[adID].append(record)
        self.dataset_camgaign[camgaignID].append(record)
        self.dataset_advertiser[advertiserID].append(record)
        self.dataset_app[appID].append(record)

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

