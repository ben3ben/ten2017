class App:
    def __init__(self, path, debug=False):
        self.debug = debug
        self.data = dict()
        self.dataset_app_cat = dict()
        self.read(path)

    def read(self, path):
        fin = open(path)
        fin.readline()
        for index, line in enumerate(fin):
            if self.debug and index >= 1000:
                break
            tmp = [int(v) for v in line.split(',')]
            appID, appCategory = tmp
            self.data[appID] = {'appID': appID,
                                'appCategory': appCategory}
        fin.close()

    def get_keys(self):
        return list(self.data.keys())

    def get_value(self, key):
        return self.data[key]

    def exists(self, key):
        return key in self.data

    def add_dataset(self, record, appCategory):
        if appCategory not in self.dataset_app_cat:
            self.dataset_app_cat[appCategory] = list()
        self.dataset_app_cat[appCategory].append(record)

    def get_dataset(self, appCategory):
        return self.dataset_app_cat[appCategory]