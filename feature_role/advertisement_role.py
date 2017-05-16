from reading.dataset import Dataset
from reading.advertisement import Advertisement
from conf.configure import Configure
from handle.handle import handle_correlate_to_vec


class Advertisement_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set, ad):
        self.data_set = data_set  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.fea_set = dict()
        self.ad_corr = {'train': self.read_correlate(Configure.advertiser_correlate['train']),
                        'test': self.read_correlate(Configure.advertiser_correlate['test']),
                        'submit': self.read_correlate(Configure.advertiser_correlate['submit'])}
        self.camgaign_corr = {'train': self.read_correlate(Configure.camgaign_correlate['train']),
                              'test': self.read_correlate(Configure.camgaign_correlate['test']),
                              'submit': self.read_correlate(Configure.camgaign_correlate['submit'])}
        self.advertiser_corr = {'train': self.read_correlate(Configure.advertiser_correlate['train']),
                                'test': self.read_correlate(Configure.advertiser_correlate['test']),
                                'submit': self.read_correlate(Configure.advertiser_correlate['submit'])}
        self.app_corr = {'train': self.read_correlate(Configure.app_correlate['train']),
                         'test': self.read_correlate(Configure.app_correlate['test']),
                         'submit': self.read_correlate(Configure.app_correlate['submit'])}

    def read_correlate(self, path):
        result = dict()
        fin = open(path)
        for line in fin:
            tmp = [int(v) for v in line.strip().split(',')]
            if tmp[0] not in result:
                result[tmp[0]] = dict()
            result[tmp[0]][tmp[1]] = tmp[2:]
        fin.close()
        return result

    def get_fea_names(self):
        return Advertisement_Role.fea_names

    def appPlatform_to_vec(self, appPlatform):
        return [appPlatform]

    # not user directly
    def click_count_operator(self, dlist, _time, tw):
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['clickTime']
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                result[index] += 1
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    # not use directly
    def convert_count_operator(self, dlist, _time, tw):
        r = len(dlist)
        while r > 0 and dlist[r - 1]['clickTime'] >= _time:
            r -= 1
        result = [0] * len(tw)
        index = 0
        if r > 0:
            for d in dlist[r - 1::-1]:
                diff = _time - d['clickTime']
                # print(d['clickTime'])
                while index < len(tw) and diff > tw[index]:
                    index += 1
                if index == len(tw):
                    break
                result[index] += d['label']
        for i in range(1, len(tw)):
            result[i] += result[i - 1]
        return result

    # not user directly
    def convert_ratio_operator(self, dlist, _time, tw):
        convert = self.convert_count_operator(dlist, _time, tw)
        click = self.click_count_operator(dlist, _time, tw)
        result = [a / (b + a + 1) for a, b in zip(convert, click)]
        return result

    def create_click_count(self, creativeID, _time, tw):
        return self.click_count_operator(self.ad.get_dataset_create(creativeID), _time, tw)

    def create_convert_count(self, creativeID, _time, tw):
        return self.convert_count_operator(self.ad.get_dataset_create(creativeID), _time, tw)

    def create_convert_ratio(self, creativeID, _time, tw):
        return self.convert_ratio_operator(self.ad.get_dataset_create(creativeID), _time, tw)

    def ad_click_count(self, adID, _time, tw):
        return self.click_count_operator(self.ad.get_dataset_ad(adID), _time, tw)

    def ad_convert_count(self, adID, _time, tw):
        return self.convert_count_operator(self.ad.get_dataset_ad(adID), _time, tw)

    def ad_convert_ratio(self, adID, _time, tw):
        return self.convert_ratio_operator(self.ad.get_dataset_ad(adID), _time, tw)

    def camgaign_click_count(self, camgaignID, _time, tw):
        return self.click_count_operator(self.ad.get_dataset_camgaign(camgaignID), _time, tw)

    def camgaign_convert_count(self, camgaignID, _time, tw):
        return self.convert_count_operator(self.ad.get_dataset_camgaign(camgaignID), _time, tw)

    def camgaign_convert_ratio(self, camgaignID, _time, tw):
        return self.convert_ratio_operator(self.ad.get_dataset_camgaign(camgaignID), _time, tw)

    def advertiser_click_count(self, advertiserID, _time, tw):
        return self.click_count_operator(self.ad.get_dataset_advertiser(advertiserID), _time, tw)

    def advertiser_convert_count(self, advertiserID, _time, tw):
        return self.convert_count_operator(self.ad.get_dataset_advertiser(advertiserID), _time, tw)

    def advertiser_convert_ratio(self, advertiserID, _time, tw):
        return self.convert_ratio_operator(self.ad.get_dataset_advertiser(advertiserID), _time, tw)

    def app_click_count(self, appID, _time, tw):
        return self.click_count_operator(self.ad.get_dataset_app(appID), _time, tw)

    def app_convert_count(self, appID, _time, tw):
        return self.convert_count_operator(self.ad.get_dataset_app(appID), _time, tw)

    def app_convert_ratio(self, appID, _time, tw):
        return self.convert_ratio_operator(self.ad.get_dataset_app(appID), _time, tw)

    def to_dlist_of_correlate(self, dlist, cond_name):
        result = list()
        for d in dlist:
            _r = {'label': d['label'],
                  'clickTime': d['clickTime'],
                  cond_name: self.ad.get_value(d['creativeID'])[cond_name]}
            result.append(_r)
        return result

    def ad_correlate(self, userID, adID, clickDay, mode):
        cond_name = 'adID'
        dlist = self.to_dlist_of_correlate(self.data_set.get_value_by_user_id(userID), cond_name)
        correlate = self.ad_corr[mode]
        return handle_correlate_to_vec(correlate, dlist, cond_name, adID, clickDay)

    def camgaign_correlate(self, userID, camgaignID, clickDay, mode):
        cond_name = 'camgaignID'
        dlist = self.to_dlist_of_correlate(self.data_set.get_value_by_user_id(userID), cond_name)
        correlate = self.camgaign_corr[mode]
        return handle_correlate_to_vec(correlate, dlist, cond_name, camgaignID, clickDay)

    def advertiser_correlate(self, userID, advertiserID, clickDay, mode):
        cond_name = 'advertiserID'
        dlist = self.to_dlist_of_correlate(self.data_set.get_value_by_user_id(userID), cond_name)
        correlate = self.advertiser_corr[mode]
        return handle_correlate_to_vec(correlate, dlist, cond_name, advertiserID, clickDay)

    def app_correlate(self, userID, appID, clickDay, mode):
        cond_name = 'appID'
        dlist = self.to_dlist_of_correlate(self.data_set.get_value_by_user_id(userID), cond_name)
        correlate = self.app_corr[mode]
        return handle_correlate_to_vec(correlate, dlist, cond_name, appID, clickDay)

    def get_key(self, *args):
        return ';'.join([str(v) for v in args])

    def generate(self, func, scope, save, *args):
        key = self.get_key(scope, *args)
        if save and key in self.fea_set:
            return self.fea_set[key]
        fea = func(*args)
        if save:
            self.fea_set[key] = fea
        if not Advertisement_Role.flag:
            for index in range(len(fea)):
                Advertisement_Role.fea_names.append('{}_{}'.format(scope, index))
        return fea

    def run(self, param):
        result = list()
        creativeID = param['creativeID']
        create = self.ad.get_value(creativeID)
        adID = create['adID']
        camgaignID = create['camgaignID']
        advertiserID = create['advertiserID']
        appID = create['appID']
        appPlatform = create['appPlatform']
        result.extend(self.generate(self.appPlatform_to_vec, 'ad_appPlatform', False, appPlatform))

        result.extend(self.generate(self.create_click_count, 'ad_dataset_create_click_count', True,
                                    creativeID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.create_convert_count, 'ad_dataset_create_convert_count', True,
                                    creativeID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.create_convert_ratio, 'ad_dataset_create_convert_ratio', True,
                                    creativeID, param['clickDay'], Configure.days_windows))

        result.extend(self.generate(self.ad_click_count, 'ad_dataset_ad_click_count', True,
                                    adID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.ad_convert_count, 'ad_dataset_ad_convert_count', True,
                                    adID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.ad_convert_ratio, 'ad_dataset_ad_convert_ratio', True,
                                    adID, param['clickDay'], Configure.days_windows))

        result.extend(self.generate(self.camgaign_click_count, 'ad_dataset_camgaign_click_count', True,
                                    camgaignID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.camgaign_convert_count, 'ad_dataset_camgaign_convert_count', True,
                                    camgaignID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.camgaign_convert_ratio, 'ad_dataset_camgaign_convert_ratio', True,
                                    camgaignID, param['clickDay'], Configure.days_windows))

        result.extend(self.generate(self.advertiser_click_count, 'ad_dataset_advertiser_click_count', True,
                                    advertiserID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.advertiser_convert_count, 'ad_dataset_advertiser_convert_count', True,
                                    advertiserID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.advertiser_convert_ratio, 'ad_dataset_advertiser_convert_ratio', True,
                                    advertiserID, param['clickDay'], Configure.days_windows))

        result.extend(self.generate(self.app_click_count, 'ad_dataset_app_click_count', True,
                                    appID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.app_convert_count, 'ad_dataset_app_convert_count', True,
                                    appID, param['clickDay'], Configure.days_windows))
        result.extend(self.generate(self.app_convert_ratio, 'ad_dataset_app_convert_ratio', True,
                                    appID, param['clickDay'], Configure.days_windows))

        # '''correlate features'''
        # result.extend(self.generate(self.ad_correlate, 'ad_correlate', True,
        #                             param['userID'], adID, param['clickTime'], param['mode']))
        # result.extend(self.generate(self.camgaign_correlate, 'camgaign_correlate', True,
        #                             param['userID'], camgaignID, param['clickTime'], param['mode']))
        # result.extend(self.generate(self.advertiser_correlate, 'advertiser_correlate', True,
        #                             param['userID'], advertiserID, param['clickTime'], param['mode']))
        # result.extend(self.generate(self.app_correlate, 'app_correlate', True,
        #                             param['userID'], appID, param['clickTime'], param['mode']))

        Advertisement_Role.flag = True
        return result
