import xgboost as xgb
from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    debug = False
    print('reading data...')
    ad = Advertisement(Configure.ad_path, debug=debug)
    app = App(Configure.app_categories_path, debug=debug)
    data_set = Dataset(Configure.train_path, Configure.test_path, debug=debug)
    position = Position(Configure.position_path, debug=debug)
    user = User(Configure.user_path, debug=debug)
    user_app_actions = User_App_Actions(Configure.user_app_actions_path, debug=debug)

    days = [0] * 32
    hours = [0] * 24
    minutes = [0] * 60

    conver_days = [0] * 32
    conver_hours = [0] * 24
    conver_minutes = [0] * 60

    click_in_con_days=  [0] * 32
    click_in_con_hours = [0] * 24
    click_in_con_minutes = [0] * 60
    for v in data_set.get_data_list():
        click = v['clickTime']
        days[click // 10000] += 1
        hours[click // 100 % 100] += 1
        minutes[click % 100] += 1

        if 'conversionTime' not in v:
            continue
        conver = v['conversionTime']
        if conver == -1:
            continue
        conver_days[conver // 10000] += 1
        conver_hours[conver // 100 % 100] += 1
        conver_minutes[conver % 100] += 1

        click_in_con_days[click // 10000] += 1
        click_in_con_hours[click // 100 % 100] += 1
        click_in_con_minutes[click % 100] += 1

    plt.subplot(411)
    plt.title('click times')
    plt.plot(minutes)
    plt.subplot(412)
    plt.title('conversionTime')
    plt.plot(conver_minutes)
    plt.subplot(413)
    plt.title('click in conversion')
    plt.plot(click_in_con_minutes)
    plt.subplot(414)
    plt.title('click in conversion ratio')
    plt.plot(np.array(click_in_con_minutes) / np.array(minutes))
    plt.show()

