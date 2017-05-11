from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed

def f(*args):
    print(args)
    print(';'.join([str(v) for v in args]))

def g(func=None, *args):
    print(*args)
    print(args)
    for i in args:
        print(i)
    print(func.__name__)
    f(func.__name__, *args)
if __name__ == '__main__':
    g(f, 1, 2)
    print('{0:} {1:0.2f}'.format(0.111111111, 0.12312321))