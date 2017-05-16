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
    data_set = Dataset(Configure.train_path, Configure.test_path)
    data_set.output_by_userid(Configure.dataset_sort_by_userid)



