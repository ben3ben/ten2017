import numpy as np
from reading.dataset import Dataset
from reading.advertisement import Advertisement
from conf.configure import Configure
from handle.handle import handle_correlate_to_vec
from handle.handle import delta_time
import scipy

class Advertisement_Role:
    flag = False
    fea_names = list()

    def __init__(self, data_set, ad):
        self.data_set = data_set  # type: Dataset
        self.ad = ad  # type: Advertisement
        self.fea_set = dict()
        self.app_set = self.read_app_set()

    def read_app_set(self):
        result = dict()
        for key in self.ad.get_keys():
            record = self.ad.get_value(key)
            creativeID = record.creativeID
            adID = record.adID
            camgaignID = record.camgaignID
            advertiserID = record.advertiserID
            appID = record.appID
            if appID not in result:
                result[appID] = dict()
                result[appID]['creative'] = set()
                result[appID]['ad'] = set()
                result[appID]['camgaign'] = set()
                result[appID]['advertiser'] = set()
            result[appID]['creative'].add(creativeID)
            result[appID]['ad'].add(adID)
            result[appID]['camgaign'].add(camgaignID)
            result[appID]['advertiser'].add(advertiserID)
        return result

    def get_fea_names(self):
        return Advertisement_Role.fea_names

    def appPlatform_to_vec(self, appPlatform):
        return [appPlatform]

    def create_click_count(self, creativeID, _time, tw):
        return [self.ad.get_create_count(creativeID, 0, _time - tw, _time)]

    def create_convert_count(self, creativeID, _time, tw):
        return [self.ad.get_create_count(creativeID, 1, _time - tw, _time)]

    def create_convert_ratio(self, creativeID, _time, tw):
        convert = self.ad.get_create_count(creativeID, 1, _time - tw, _time)
        _sum = self.ad.get_create_count(creativeID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def ad_click_count(self, adID, _time, tw):
        return [self.ad.get_ad_count(adID, 0, _time - tw, _time)]

    def ad_convert_count(self, adID, _time, tw):
        return [self.ad.get_ad_count(adID, 1, _time - tw, _time)]

    def ad_convert_ratio(self, adID, _time, tw):
        convert = self.ad.get_ad_count(adID, 1, _time - tw, _time)
        _sum = self.ad.get_ad_count(adID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def camgaign_click_count(self, camgaignID, _time, tw):
        return [self.ad.get_camgaign_count(camgaignID, 0, _time - tw, _time)]

    def camgaign_convert_count(self, camgaignID, _time, tw):
        return [self.ad.get_camgaign_count(camgaignID, 1, _time - tw, _time)]

    def camgaign_convert_ratio(self, camgaignID, _time, tw):
        convert = self.ad.get_camgaign_count(camgaignID, 1, _time - tw, _time)
        _sum = self.ad.get_camgaign_count(camgaignID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def advertiser_click_count(self, advertiserID, _time, tw):
        return [self.ad.get_advertiser_count(advertiserID, 0, _time - tw, _time)]

    def advertiser_convert_count(self, advertiserID, _time, tw):
        return [self.ad.get_advertiser_count(advertiserID, 1, _time - tw, _time)]

    def advertiser_convert_ratio(self, advertiserID, _time, tw):
        convert = self.ad.get_advertiser_count(advertiserID, 1, _time - tw, _time)
        _sum = self.ad.get_advertiser_count(advertiserID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def app_click_count(self, appID, _time, tw):
        return [self.ad.get_app_count(appID, 0, _time - tw, _time)]

    def app_convert_count(self, appID, _time, tw):
        return [self.ad.get_app_count(appID, 1, _time - tw, _time)]

    def app_convert_ratio(self, appID, _time, tw):
        convert = self.ad.get_app_count(appID, 1, _time - tw, _time)
        _sum = self.ad.get_app_count(appID, -1, _time - tw, _time)
        return [convert / (_sum + 1)]

    def app_convert_time_len(self, appID, clickDay):
        s = list()
        for d in self.ad.get_dataset_app(appID):
            if d.clickTime >= clickDay:
                break
            if d.label == 1:
                s.append(delta_time(d.conversionTime, d.clickTime))
        return [np.average(s)] if len(s) > 0 else [-1]

    def creative_convert_time_len(self, creativeID, clickDay):
        s = list()
        for d in self.ad.get_dataset_create(creativeID):
            if d.clickTime >= clickDay:
                break
            if d.label == 1:
                s.append(delta_time(d.conversionTime, d.clickTime))
        return [np.average(s)] if len(s) > 0 else [-1]

    def app_set_to_vec(self, appID):
        _keys = ['creative', 'ad', 'camgaign', 'advertiser']
        result = [len(self.app_set[appID][k]) for k in _keys]
        return result

    def app_convert_ratio_27day(self, appID, _day, tw):
        _sum = 0
        for i in range(tw):
            convert = self.ad.get_app_count(appID, 1, _day - i - 1, _day - i)
            click = self.ad.get_app_count(appID, 0, _day - i - 1, _day - i)
            _sum += convert / (click + convert + 1)
        return [_sum / tw]

    def app_convert_ratio_var(self, appID, _day, tw):
        cr = list()
        for i in range(tw):
            convert = self.ad.get_app_count(appID, 1, _day - i - 1, _day - i)
            click = self.ad.get_app_count(appID, 0, _day - i - 1, _day - i)
            cr.append(convert / (click + convert + 1))
        return [scipy.var(cr)]

    def app_click_var(self, appID, _day, tw):
        cr = list()
        for i in range(tw):
            click = self.ad.get_app_count(appID, 0, _day - i - 1, _day - i)
            cr.append(click)
        return [scipy.var(cr)]

    def create_convert_ratio_median(self, creativeID, _day, tw):
        cr = list()
        for i in range(tw):
            convert = self.ad.get_create_count(creativeID, 1, _day - i - 1, _day - i)
            click = self.ad.get_create_count(creativeID, 0, _day - i - 1, _day - i)
            cr.append(convert / (click + convert + 1))
        return [scipy.median(cr)]

    def app_convert_ratio_median(self, appID, _day, tw):
        cr = list()
        for i in range(tw):
            convert = self.ad.get_app_count(appID, 1, _day - i - 1, _day - i)
            click = self.ad.get_app_count(appID, 0, _day - i - 1, _day - i)
            cr.append(convert / (click + convert + 1))
        return [scipy.median(cr)]

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
        adID = param['adID']
        camgaignID = param['camgaignID']
        advertiserID = param['advertiserID']
        appID = param['appID']
        appPlatform = param['appPlatform']
        clickDay = param['clickDay']
        _day = clickDay // 10000
        result.extend(self.generate(self.appPlatform_to_vec, 'ad_appPlatform', False, appPlatform))

        for tw in Configure.days_windows:
            _tw = tw // 10000
            # result.extend(self.generate(self.create_click_count, 'ad_create_click_count_{}'.format(tw), True,
            #                             creativeID, _day, _tw))
            result.extend(self.generate(self.create_convert_ratio, 'ad_create_convert_ratio_{}'.format(tw), True,
                                        creativeID, _day, _tw))

            result.extend(self.generate(self.ad_convert_count, 'ad_ad_convert_count_{}'.format(tw), True,
                                        adID, _day, _tw))
            result.extend(self.generate(self.ad_convert_ratio, 'ad_ad_convert_ratio_{}'.format(tw), True,
                                        adID, _day, _tw))

            # result.extend(self.generate(self.camgaign_click_count, 'ad_camgaign_click_count_{}'.format(tw), True,
            #                             camgaignID, _day, _tw))
            # result.extend(self.generate(self.camgaign_convert_count, 'ad_camgaign_convert_count_{}'.format(tw), True,
            #                             camgaignID, _day, _tw))
            result.extend(self.generate(self.camgaign_convert_ratio, 'ad_camgaign_convert_ratio_{}'.format(tw), True,
                                        camgaignID, _day, _tw))

            result.extend(self.generate(self.advertiser_click_count, 'ad_advertiser_click_count_{}'.format(tw), True,
                                        advertiserID, _day, _tw))
            result.extend(self.generate(self.advertiser_convert_count, 'ad_advertiser_convert_count_{}'.format(tw), True,
                                        advertiserID, _day, _tw))
            result.extend(self.generate(self.advertiser_convert_ratio, 'ad_advertiser_convert_ratio_{}'.format(tw), True,
                                        advertiserID, _day, _tw))

            result.extend(self.generate(self.app_click_count, 'ad_app_click_count_{}'.format(tw), True,
                                        appID, _day, _tw))
            result.extend(self.generate(self.app_convert_count, 'ad_app_convert_count_{}'.format(tw), True,
                                        appID, _day, _tw))
            result.extend(self.generate(self.app_convert_ratio, 'ad_app_convert_ratio_{}'.format(tw), True,
                                        appID, _day, _tw))
            result.extend(self.generate(self.create_convert_ratio_median, 'ad_create_cr_median_{}'.format(tw), True,
                                        creativeID, _day, _tw))
            result.extend(self.generate(self.app_convert_ratio_median, 'ad_app_cr_median_{}'.format(tw), True,
                                        appID, _day, _tw))

        result.extend(self.generate(self.app_convert_time_len, 'app_convert_time_len', True, appID, clickDay))
        result.extend(self.generate(self.creative_convert_time_len, 'creative_convert_time_len', True, creativeID, clickDay))
        result.extend(self.generate(self.app_set_to_vec, 'app_set_to_vec', True, appID))

        for tw in [1, 3, 5]:
            result.extend(self.generate(self.app_convert_ratio_27day, 'convert_ratio_27day_{}'.format(tw), True,
                                        appID, 28, tw))

        Advertisement_Role.flag = True
        return result
