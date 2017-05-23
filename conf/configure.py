from sklearn.metrics import roc_auc_score


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

    xgb_model_file = {'model': '../../file/model/xgb/xgb.model',
                      'train': '../../file/model/xgb/train_save.csv',
                      'test': '../../file/model/xgb/test_save.csv',
                      'submit': '../../file/model/xgb/submit_save.csv'}
    xgb_diff_model_file = {'model': '../../file/model/xgb_diff/xgb_diff.model',
                           'train': '../../file/model/xgb_diff/train_diff.csv',
                           'test': '../../file/model/xgb_diff/test_diff.csv',
                           'submit': '../../file/model/xgb_diff/submit_diff.csv'}
    xgb_kflod_model_file = {'model': '../../file/model/kflod/xgb_kflod.model',
                            'train': '../../file/model/kflod/train_kflod.csv',
                            'test': '../../file/model/kflod/test_kflod.csv',
                            'submit': '../../file/model/kflod/submit_kflod.csv'}

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
    cate_app_correlate = '../../file/merge_correlate/cate_app_correlate_{}_{}.csv'
    '''feature files'''
    feature_files = {'train': '../../file/feature/train_feature.csv',
                     'train_describe': '../../file/feature/train_feature_describe.csv',
                     'test': '../../file/feature/test_feature.csv',
                     'test_describe': '../../file/feature/test_feature_describe.csv',
                     'submit': '../../file/feature/submit_feature.csv',
                     'submit_describe': '../../file/feature/submit_feature_describe.csv'}
    xgb_feature = {'xgb_train': '../../file/dmatrix/xbg.train',
                   'train_instanceID': '../../file/dmatrix/train_instanceID.csv',
                   'xgb_test': '../../file/dmatrix/xbg.test',
                   'test_instanceID': '../../file/dmatrix/test_instanceID.csv',
                   'xgb_submit': '../../file/dmatrix/xbg.submit',
                   'submit_instanceID': '../../file/dmatrix/submit_instanceID.csv',
                   'feature_names':  '../../file/dmatrix/feature_names.csv'}

    '''lda'''
    user_appid_topic_for_user = '../../data/lda/user_appid_topic_for_user.csv'
    user_appid_topic_for_appid = '../../data/lda/user_appid_topic_for_appid.csv'
    '''submission'''
    submission = '../../file/submit/submission.csv'

    '''session 1'''
    train_begin_t = 280000
    train_end_t = 300000
    test_begin_t = 300000
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

    minutes_windows = [50000, 70000, 100000]
    days_windows = [50000, 70000, 100000]

    '''features erase'''
    features_erase = ['position_positionType_5', 'cate_baby_corr_10000_0', 'user_create_click_count_0',
                      'position_positionType_3', 'user_ad_click_count_0', 'position_sitesetID_2',
                      'user_create_click_count_2']
    features_erase.extend(['user_ad_click_count_1',
                           'cate_hour_corr_10000_0', 'app_baby_corr_10000_0',
                           'dataset_connectionType_4', 'app_cate_split_in_hours_30000_1', 'creative_convert_time_len_0',
                           'position_positionType_4', 'position_positionType_2', 'dataset_connectionType_0',
                           'app_actions_install_count_1', 'user_appID_convert_count_0',
                           'dataset_connectionType_2', 'dataset_connectionType_3', 'app_cate_split_in_hours_30000_0',
                           'user_advertiserID_click_count_0', 'user_appID_click_count_0'])
    features_erase.extend(['app_baby_corr_30000_1'])
    features_erase.extend(
        ['app_cate_to_vec_3', 'app_cate_to_vec_5', 'user_camgaignID_click_count_0', 'user_convert_time_len_0'])

    features_erase.extend(['user_all_diff_1_0', 'user_all_diff_5_0', 'ad_ad_convert_count_50000_0',
                           'user_havebaby_6'])
    features_erase.extend(['user_create_click_count_1', 'ad_ad_convert_count_70000_0', 'user_ad_click_count_2',
                           'ad_advertiser_click_count_70000_0'])

    features_erase.extend(['user_dataset_click_one_day_17', 'user_residence_convert_ratio_50000_0', 'user_marriage_0',
                           'user_edu_4', 'user_dataset_click_in_days_0', 'user_residence_click_count_70000_0',
                           'app_baby_corr_150000_1', 'app_cate_dataset_click_count_1', 'user_havebaby_1',
                           'user_marriage_2', 'user_edu_0', 'user_age_4', 'user_age_2', 'app_cate_dataset_convert_count_2',
                           'user_marriage_3', 'dataset_clicktime_6', 'user_age_1', 'user_appID_convert_ratio_0',
                           'user_convert_ratio_70000_0', 'user_appID_convert_count_2', 'user_dataset_click_one_day_18',
                           'user_op_type_ratio_1', 'user_havebaby_2', 'dataset_clicktime_2', 'user_age_6',
                           'user_edu_5', 'user_convert_count_50000_0', 'user_age_7', 'user_havebaby_5',
                           'user_dataset_click_one_day_14', 'user_convert_ratio_50000_0', 'user_appPlatform_convert_count_0',
                           'user_havebaby_4', 'user_appID_op_set_1', 'user_appPlatform_convert_count_2',
                           'user_appID_convert_ratio_1', 'user_appID_convert_count_1'])
