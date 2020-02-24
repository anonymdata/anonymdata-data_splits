import sys
import os
import math
import random
import numpy as np
import pandas as pd
import sklearn

sys.path.append("../")

import utils.constants as Constants
from utils.unigramTable import UnigramTable

# indicators of the colunmn name
DEFAULT_USER_COL = Constants.DEFAULT_USER_COL
DEFAULT_ITEM_COL = Constants.DEFAULT_ITEM_COL
DEFAULT_ORDER_COL = Constants.DEFAULT_ORDER_COL
DEFAULT_RATING_COL = Constants.DEFAULT_RATING_COL
DEFAULT_LABEL_COL = Constants.DEFAULT_LABEL_COL
DEFAULT_TIMESTAMP_COL = Constants.DEFAULT_TIMESTAMP_COL
DEFAULT_PREDICTION_COL = Constants.DEFAULT_PREDICTION_COL
DEFAULT_FLAG_COL = Constants.DEFAULT_FLAG_COL

par_abs_dir = os.path.abspath(os.path.join(os.path.abspath("."), os.pardir))


def load_data(data_dir, max_id=0, leave_one_item=False):
    loaded = np.load(os.path.join(data_dir, "train.npz"))
    train_df = pd.DataFrame(
        data={
            DEFAULT_USER_COL: loaded["user_ids"],
            DEFAULT_ITEM_COL: loaded["item_ids"],
            DEFAULT_ORDER_COL: loaded["order_ids"],
            DEFAULT_RATING_COL: loaded["ratings"],
            DEFAULT_TIMESTAMP_COL: loaded["timestamp"],
        }
    )
    if max_id:
        train_df = train_df[
            (train_df[DEFAULT_USER_COL] < max_id)
            & (train_df[DEFAULT_ITEM_COL] < max_id)
        ]
    valid_dfs = []
    test_dfs = []
    for i in range(10):
        loaded = np.load(os.path.join(data_dir, "valid_" + str(i) + ".npz"))
        valid_df = pd.DataFrame(
            data={
                DEFAULT_USER_COL: loaded["user_ids"],
                DEFAULT_ITEM_COL: loaded["item_ids"],
                DEFAULT_RATING_COL: loaded["ratings"],
            }
        )
        if max_id:
            valid_df = valid_df[
                (valid_df[DEFAULT_USER_COL] < max_id)
                & (valid_df[DEFAULT_ITEM_COL] < max_id)
            ]
        loaded = np.load(os.path.join(data_dir, "test_" + str(i) + ".npz"))
        test_df = pd.DataFrame(
            data={
                DEFAULT_USER_COL: loaded["user_ids"],
                DEFAULT_ITEM_COL: loaded["item_ids"],
                DEFAULT_RATING_COL: loaded["ratings"],
            }
        )
        if max_id:
            test_df = test_df[
                (test_df[DEFAULT_USER_COL] < max_id)
                & (test_df[DEFAULT_ITEM_COL] < max_id)
            ]
        if leave_one_item:
            valid_df = valid_df[valid_df[DEFAULT_RATING_COL] != 1].append(
                valid_df[valid_df[DEFAULT_RATING_COL] == 1].drop_duplicates(
                    [DEFAULT_USER_COL, DEFAULT_RATING_COL]
                )
            )
            test_df = test_df[test_df[DEFAULT_RATING_COL] != 1].append(
                test_df[test_df[DEFAULT_RATING_COL] == 1].drop_duplicates(
                    [DEFAULT_USER_COL, DEFAULT_RATING_COL]
                )
            )
        valid_dfs.append(valid_df)
        test_dfs.append(test_df)
    return train_df, valid_dfs, test_dfs


def load_leave_one_item(root_dir=par_abs_dir, max_id=0):
    leave_one_out_dir = "datasets/tafeng/leave_one_item"
    data_file = os.path.join(root_dir, leave_one_out_dir)
    print("loading ta-feng dataset using leave_one_item split")
    return load_data(data_file, max_id, leave_one_item=True)


def load_leave_one_out(root_dir=par_abs_dir, max_id=0):
    leave_one_out_dir = "datasets/tafeng/leave_one_basket"
    data_file = os.path.join(root_dir, leave_one_out_dir)
    print("loading ta-feng dataset using leave_one_out split")
    return load_data(data_file, max_id)


def load_leave_one_basket(root_dir=par_abs_dir, max_id=0):
    leave_one_out_dir = "datasets/tafeng/leave_one_basket"
    data_file = os.path.join(root_dir, leave_one_out_dir)
    print("loading ta-feng dataset using leave_one_basket split")
    return load_data(data_file, max_id)


def load_temporal(root_dir=par_abs_dir, max_id=0, test_percent=None):
    temporal_dir = "datasets/tafeng/temporal"
    print("loading ta-feng dataset using temporal split")
    data_file = os.path.join(root_dir, temporal_dir)
    if test_percent != None:
        if test_percent < 1:
            test_percent = int(test_percent * 100)
        data_file = os.path.join(data_file, str(test_percent))
        print("split percent:", test_percent)
    return load_data(data_file, max_id)