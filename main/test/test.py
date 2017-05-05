from conf.configure import Configure
from reading.advertisement import Advertisement
from reading.app import App
from reading.dataset import Dataset
from reading.position import Position
from reading.user import User
from reading.user_app_actions import User_App_Actions
from reading.user_app_installed import User_App_Installed

if __name__ == '__main__':
    ad = Advertisement(Configure.ad_path, debug=True)
    app = App(Configure.app_categories_path, debug=True)
    train_set = Dataset(Configure.train_path, debug=True)
    test_set = Dataset(Configure.test_path, debug=True)
    position = Position(Configure.position_path, debug=True)
    user = User(Configure.user_path, debug=True)
    user_app_actions = User_App_Actions(Configure.user_app_actions_path, debug=True)
    user_app_installed = User_App_Installed(Configure.user_installedapps_path, debug=True)