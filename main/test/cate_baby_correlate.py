import pandas as pd
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.dataset import Dataset
from reading.user import User
from reading.app import App


if __name__ == '__main__':
    # ad = pd.read_csv(Configure.ad_path)
    # data_set = pd.read_csv(Configure.train_path)
    # user = pd.read_csv(Configure.user_path)
    # app = pd.read_csv(Configure.app_categories_path)
    #
    # data = data_set.merge(user, how='left', on='userID')
    # data = data.merge(ad, how='left', on='creativeID')
    # data = data.merge(app, how='left', on='appID')
    # data = data[data['label'] >= 0]
    # g = data.groupby(['appCategory', 'haveBaby', 'label']).count()
    # for group_name, df in g:
    #     print(group_name, df)

    ad = Advertisement(Configure.ad_path)
    app = App(Configure.app_categories_path)
    data_set = Dataset(Configure.train_path, Configure.test_path)
    user = User(Configure.user_path)

    from_t = 270000
    end_t = 290000
    result = dict()
    for d in data_set.get_data_list():
        creativeID = d['creativeID']
        userID = d['userID']
        haveBaby = user.get_value(userID)['haveBaby']
        appID = ad.get_value(creativeID)['appID']
        appCategory = app.get_value(appID)['appCategory']
        label = d['label']
        clickTime = d['clickTime']
        if clickTime < from_t or clickTime >= end_t:
            continue
        if appCategory not in result:
            result[appCategory] = dict()
        if haveBaby not in result[appCategory]:
            result[appCategory][haveBaby] = [0] * 2
        result[appCategory][haveBaby][label] += 1

    fout = open(Configure.cate_app_correlate.format(from_t, end_t), 'w')
    for cate in result:
        for app in result[cate]:
            s = result[cate][app]
            r = s[1] / (s[1] + s[0]) if s[1] > 0 else 0
            fout.write('{},{},{},{},{}\n'.format(cate, app, s[0], s[1], r))
    fout.close()


