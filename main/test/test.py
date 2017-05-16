from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed
import pandas as pd
import numpy as np


if __name__ == '__main__':
    s = np.array([[1,2,3],[4,5,6]])
    c = ['a', 'b', 'd']
    p = pd.DataFrame(data=s, columns=c)
    print(p)
    a = p.describe()
    a = a.T
    print(a)