
import os
import sys

import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.metrics import make_scorer
from sklearn.model_selection import StratifiedKFold
# import configFYP as config
import configFYPFixedHashing as config
from metrics import gini_norm
# from DataReaderFYPPredict import FeatureDictionary, DataParser
from DataReader import FeatureDictionary, DataParser
sys.path.append("..")
from DeepFM import DeepFM

gini_scorer = make_scorer(gini_norm, greater_is_better=True, needs_proba=True)


def _load_data():

    dfTrain = pd.read_csv(config.TRAIN_FILE)
    dfTest = pd.read_csv(config.TEST_FILE)

    dfTest2=pd.read_csv('predict/predict.csv')
    print(list(dfTrain.dtypes))
    print(list(dfTest.dtypes))
    print(list(dfTest2.dtypes))
    # dfTest2=pd.read_csv('predict/FYPtestUpdate.csv')
    def preprocess(df):
        cols = [c for c in df.columns if c not in ["target","id"]]
        df["missing_feat"] = np.sum((df[cols] == -1).values, axis=1)
        # df["ps_car_13_x_ps_reg_03"] = df["ps_car_13"] * df["ps_reg_03"]
        return df

    dfTrain = preprocess(dfTrain)
    dfTest = preprocess(dfTest)
    dfTest2=preprocess(dfTest2)
    cols = [c for c in dfTrain.columns if c not in ["target","id"]]
    cols = [c for c in cols if (not c in config.IGNORE_COLS)]

    X_train = dfTrain[cols].values
    y_train = dfTrain["target"].values
    # X_test = dfTest[cols].values
    # ids_test = dfTest["id"].values
    # cat_features_indices = [i for i,c in enumerate(cols) if c in config.CATEGORICAL_COLS]

    return dfTrain, dfTest, X_train, y_train, dfTest2


def get_deep_fm_model(dfTrain, dfTest, dfm_params,dfTest2):
    # fd = FeatureDictionary(dfTrain=dfTrain, dfTest=dfTest,
    #                        numeric_cols=config.NUMERIC_COLS,
    #                        ignore_cols=config.IGNORE_COLS)
    # data_parser = DataParser(feat_dict=fd)
    # # Xi_train, Xv_train, y_train = data_parser.parse(df=dfTrain, has_label=True)
    # # Xi_test, Xv_test, ids_test = data_parser.parse(df=dfTest)
    # Xi_test, Xv_test, ids_test = data_parser.parse(df=dfTest2)
    # print(fd.feat_dim)
    dfm_params["feature_size"] = 3024
    # print(len(Xi_train[0]))
    dfm_params["field_size"] = 74

    # y_train_meta = np.zeros((dfTrain.shape[0], 1), dtype=float)
    # y_test_meta = np.zeros((dfTest.shape[0], 1), dtype=float)
    # gini_results_epoch_train = np.zeros((len(folds), dfm_params["epoch"]), dtype=float)
    # gini_results_epoch_valid = np.zeros((len(folds), dfm_params["epoch"]), dtype=float)
    dfm = DeepFM(**dfm_params)

    # for i, (train_idx, valid_idx) in enumerate(folds):
        # Xi_train_, Xv_train_, y_train_ = _get(Xi_train, train_idx), _get(Xv_train, train_idx), _get(y_train, train_idx)
        # Xi_valid_, Xv_valid_, y_valid_ = _get(Xi_train, valid_idx), _get(Xv_train, valid_idx), _get(y_train, valid_idx)
        # print(y_train)


        # print(y_train_)
        # print(dfm.predict(Xi_train_, Xv_train_))
        # continue
        # dfm.fit(Xi_train_, Xv_train_, y_train_, Xi_valid_, Xv_valid_, y_valid_)

        # y_train_meta[valid_idx, 0] = dfm.predict(Xi_valid_, Xv_valid_)
        # y_test_meta[:, 0] += dfm.predict(Xi_test, Xv_test)
        #
        # gini_results_cv[i] = gini_norm(y_valid_, y_train_meta[valid_idx])
        # gini_results_epoch_train[i] = dfm.train_result
        # gini_results_epoch_valid[i] = dfm.valid_result
        # print('saving')
        # dfm.saver.save(dfm.sess, save_path, global_step=past_epoch + dfm_params["epoch"] * (i + 1))

    # y_test_meta /= float(len(folds))

    # # save result
    # if dfm_params["use_fm"] and dfm_params["use_deep"]:
    #     clf_str = "DeepFM"
    # elif dfm_params["use_fm"]:
    #     clf_str = "FM"
    # elif dfm_params["use_deep"]:
    #     clf_str = "DNN"
    # print("%s: %.5f (%.5f)" % (clf_str, gini_results_cv.mean(), gini_results_cv.std()))
    # filename = "%s_Mean%.5f_Std%.5f.csv" % (clf_str, gini_results_cv.mean(), gini_results_cv.std())
    # _make_submission(ids_test, y_test_meta, filename)
    # gini_results_epoch_train = np.zeros((1, dfm_params["epoch"] * len(folds)), dtype=float)
    # gini_results_epoch_valid = np.zeros((1, dfm_params["epoch"] * len(folds)), dtype=float)
    # gini_results_epoch_train[0] = dfm.train_result
    # gini_results_epoch_valid[0] = dfm.valid_result
    # _plot_fig(gini_results_epoch_train, gini_results_epoch_valid, clf_str)

    return dfm


# load data
dfTrain, dfTest, X_train, y_train,dfTest2 = _load_data()

# folds
# folds = list(StratifiedKFold(n_splits=config.NUM_SPLITS, shuffle=True,
#                              random_state=config.RANDOM_SEED).split(X_train, y_train))


# ------------------ DeepFM Model ------------------
# params
dfm_params = {
    "use_fm": True,
    "use_deep": True,
    "embedding_size": 16,
    "dropout_fm": [1.0, 1.0],
    "deep_layers": [2000, 2000,1500],
    "dropout_deep": [0.5, 0.5, 0.8,0.6],
    "deep_layers_activation": tf.nn.relu,
    "epoch": 2000,#500#1500
    "batch_size": 1024,
    "learning_rate": 0.001,
    "optimizer_type": "adagrad",
    "batch_norm": 1,
    "batch_norm_decay": 0.995,
    "l2_reg": 0.01,
    "verbose": True,
    "eval_metric": gini_norm,
    "random_seed": config.RANDOM_SEED,
    "loss_type":"mse"
}
# y_train_dfm, y_test_dfm,dfm_dfm = _run_base_model_dfm(dfTrain, dfTest, folds, dfm_params,"save/dfm/temp",past_epoch=3620)
# dfm_dfm.saver.save(dfm_dfm.sess,'save/dfm',global_step=dfm_params["epoch"])

# ------------------ FM Model ------------------Backup

# fm_params = dfm_params.copy()
# fm_params["use_deep"] = False
# y_train_fm, y_test_fm,dfm_fm = _run_base_model_dfm(dfTrain, dfTest, folds, fm_params,"save/fm/temp")
# dfm_fm.saver.save(dfm_fm.sess,'save/fm',global_step=dfm_params["epoch"])

# ------------------ DNN Model ------------------
dnn_params = dfm_params.copy()
dnn_params["use_fm"] = False
dfm_dnn = get_deep_fm_model(dfTrain, dfTest, dnn_params,dfTest2)
###Convert Predict Data
from datetime import datetime
start_time=datetime.now()
fd = FeatureDictionary(dfTrain=dfTrain, dfTest=dfTest,
                       numeric_cols=config.NUMERIC_COLS,
                       ignore_cols=config.IGNORE_COLS)
data_parser = DataParser(feat_dict=fd)
Xi_test, Xv_test, _ = data_parser.parse(df=dfTest2)
print('Consumed Time for Convert Data: {} second(s)'.format(str((datetime.now()-start_time).seconds)))
###Convert Predict Data
past_epoch=800
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=1600
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=2400
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=6400
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=10400
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=14400
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])

past_epoch=34400
dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
predict_result=dfm_dnn.predict(Xi_test,Xv_test)
print(predict_result[0])