class Configure:
    ad_path = '../../data/ad.csv'
    app_categories_path = '../../data/app_categories.csv'
    position_path = '../../data/position.csv'
    test_path = '../../data/test.csv'
    train_path = '../../data/train.csv'
    user_path = '../../data/user.csv'
    user_app_actions_path = '../../data/user_app_actions.csv'
    user_installedapps_path = '../../data/user_installedapps.csv'

    xgb_feature_importance = '../../file/xgb_feature_importance.csv'
    submission = '../../file/submit/submission.csv'
    train_begin_t = 270000
    train_end_t = 290000
    test_begin_t = 290000
    test_end_t = 310000
    submit_begin_t = 310000
    submit_end_t = 320000

    minutes_windows = [100, 1200, 10000, 20000, 50000, 100000, 150000]
    days_windows = [10000, 20000, 500000, 150000]
