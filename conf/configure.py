class Configure:
    ad_path = '../../data/ad.csv'
    app_categories_path = '../../data/app_categories.csv'
    position_path = '../../data/position.csv'
    test_path = '../../data/test.csv'
    train_path = '../../data/train.csv'
    user_path = '../../data/user.csv'
    user_app_actions_path = '../../data/user_app_actions.csv'
    user_installedapps_path = '../../data/user_installedapps.csv'
    dataset_sort_by_userid = '../../data/dataset_sorted_by_userid.csv'

    xgb_model_file = '../../file/model/xgb.model'
    xgb_feature_importance = '../../file/xgb_feature_importance.csv'
    '''correlate'''
    creative_correlate = {'train': '../../file/correlate/creative_correlate_train.csv',
                          'test': '../../file/correlate/creative_correlate_test.csv',
                          'submit': '../../file/correlate/creative_correlate_submit.csv'}
    ad_correlate = {'train': '../../file/correlate/ad_correlate_train.csv',
                    'test': '../../file/correlate/ad_correlate_test.csv',
                    'submit': '../../file/correlate/ad_correlate_submit.csv'}
    camgaign_correlate = {'train': '../../file/correlate/camgaign_correlate_train.csv',
                          'test': '../../file/correlate/camgaign_correlate_test.csv',
                          'submit': '../../file/correlate/camgaign_correlate_submit.csv'}
    advertiser_correlate = {'train': '../../file/correlate/advertiser_correlate_train.csv',
                            'test': '../../file/correlate/advertiser_correlate_test.csv',
                            'submit': '../../file/correlate/advertiser_correlate_submit.csv'}
    app_correlate = {'train': '../../file/correlate/app_correlate_train.csv',
                     'test': '../../file/correlate/app_correlate_test.csv',
                     'submit': '../../file/correlate/app_correlate_submit.csv'}
    position_correlate = {'train': '../../file/correlate/position_correlate_train.csv',
                          'test': '../../file/correlate/position_correlate_test.csv',
                          'submit': '../../file/correlate/position_correlate_submit.csv'}
    '''merge correlate'''
    baby_app_correlate = '../../file/merge_correlate/baby_app_correlate_{}_{}.csv'
    '''feature files'''
    feature_files = {'train': '../../file/feature/train_feature.csv',
                     'train_describe': '../../file/feature/train_feature_describe.csv',
                     'test': '../../file/feature/test_feature.csv',
                     'test_describe': '../../file/feature/test_feature_describe.csv',
                     'submit': '../../file/feature/submit_feature.csv',
                     'submit_describe': '../../file/feature/submit_feature_describe.csv',}
    '''submission'''
    submission = '../../file/submit/submission.csv'

    '''session 1'''
    train_begin_t = 270000
    train_end_t = 290000
    test_begin_t = 290000
    test_end_t = 310000
    submit_begin_t = 310000
    submit_end_t = 320000

    '''session 2'''
    # train_begin_t = 270000
    # train_end_t = 280000
    # test_begin_t = 300000
    # test_end_t = 310000
    # submit_begin_t = 310000
    # submit_end_t = 320000

    # minutes_windows = [100, 1200, 10000, 20000, 50000, 100000, 150000]
    # days_windows = [10000, 20000, 50000, 150000]

    minutes_windows = [50000, 100000, 150000]
    days_windows = [50000, 100000, 150000]
