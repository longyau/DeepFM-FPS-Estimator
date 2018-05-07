
import os
import sys
import getopt
import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.metrics import make_scorer
from sklearn.model_selection import StratifiedKFold
sys.path.append("..")
from DeepFM import DeepFM
from metrics import gini_norm
from DataReader import FeatureDictionary, DataParser
import configFYPFixedHashing as config
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr, AttributeBase
from botocore.exceptions import ClientError
import decimal
from datetime import datetime
from urllib.parse import unquote
import hashlib
from pandas import DataFrame, Series
import sched, time
s = sched.scheduler(time.time, time.sleep)
dynamodb = boto3.resource('dynamodb')
hardware_table = dynamodb.Table('FYP_Hardware')
dfm_dnn=None
data_parser=None
past_epoch = 60400
class DynamoDBException(Exception):
    pass

class FPS(object):
    def add_info(self, name, value):
        try:
            name = name[:name.index('(')]
        except ValueError:
            pass
        self.__setattr__(name, value)

    def get_detail(self):
        return repr(self.__dict__)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def get_all_info(self):
        keys = []
        values = []
        for key, value in self.__dict__.items():
            keys.append(key)
            values.append(value)
        return keys, values

    def get_value(self, name: str):
        try:
            output = self.__getattribute__(name)
            if output is not None:
                return output
            else:
                return ''
        except AttributeError:
            return ''

    def update_value(self, key: str, newValue):
        try:
            self.__setattr__(key, newValue)
            return True
        except AttributeError:
            self.add_info(key, newValue)


def convert_decimal(o):
    if isinstance(o, decimal.Decimal):
        if o % 1 > 0:
            return float(o)
        else:
            return int(o)


def getCPUData(cpu_name: str):
    try:
        response = hardware_table.get_item(
            Key={
                'Type': 'CPU-Config',
                'Name': cpu_name
            }
        )
        item = response['Item']
        # print("GetItem succeeded:{}".format(item))
        return item
    except ClientError as e:
        print(e.response['Error']['Message'])
    except KeyError:
        return


def getGPUData(gpu_name: str):
    try:
        response = hardware_table.get_item(
            Key={
                'Type': 'GPU-Config',
                'Name': gpu_name
            }
        )
        item = response['Item']
        # print("GetItem succeeded:{}".format(item))
        return item
    except ClientError as e:
        print(e.response['Error']['Message'])
    except KeyError:
        return


def getGameData(game_name: str):
    try:
        response = hardware_table.get_item(
            Key={
                'Type': 'Game-Info',
                'Name': game_name
            }
        )
        item = response['Item']
        # print("GetItem succeeded:{}".format(item))
        return item
    except ClientError as e:
        print(e.response['Error']['Message'])
    except KeyError:
        return


def interpret_predict_FPS_Data(cpu_name: str, gpu_name: str, game_name: str, reswidth: int, resheight: int,
                           gamesetting: str, ram: int):


    file_field_string = "CPU-Score	CPU-Cache L1	CPU-Socket	CPU-Cache L3	CPU-Cache L2	CPU-Samples	CPU-Process	CPU-Brand	CPU-Cores	CPU-Type	CPU-URL	CPU-Clock	CPU-Part Number	CPU-Codename	CPU-Multi	CPU-Price	CPU-TDP	CPU-Released	CPU-Name	GPU-L2 Cache	GPU-Shader Processing Units	GPU-Process	GPU-Samples	GPU-Website	GPU-Brand	GPU-Direct X	GPU-Release Price	GPU-TMUs	GPU-PSU	GPU-ROPs	GPU-Max Power	GPU-Texture Rate	GPU-Memory	GPU-GD RATING	GPU-BenchmarkURL	GPU-Core Speed	GPU-Name	GPU-Pixel Rate	GPU-Memory Bandwidth	GPU-Shader	GPU-Name2	GPU-Power Connector	GPU-Type	GPU-Architecture	GPU-Benchmark	GPU-Memory Speed	GPU-Open GL	GPU-Memory Bus	GPU-Memory Type	GAME-Rec-DX	GAME-Website	GAME-Theme	GAME-Min-DX	GAME-Rec-Ram	GAME-Min-CPU0	GAME-Release Date2	GAME-Min-CPU1	GAME-Release Date0	GAME-Release Date1	GAME-Min-GPU1	GAME-Min-GPU0	GAME-Name	GAME-Min-VRam	GAME-Rec-CPU1	GAME-Min-OS	GAME-Rec-CPU0	GAME-Rec-GPU1	GAME-Min-Ram	GAME-Rec-GPU0	GAME-Type	GAME-Rec-OS	GAME-Rec-VRam	GAME-Genre1	GAME-Genre0	Res-Height	Res-Width	id	Game-Setting	target	Ram"
    file_field = file_field_string.split('\t')
    cpu = getCPUData(cpu_name)
    gpu = getGPUData(gpu_name)
    game = getGameData(game_name)
    if cpu is None:
        print('CPU not found')
        raise DynamoDBException('CPU not found')
    if gpu is None:
        print('GPU not found')
        raise DynamoDBException('GPU not found')
    if game is None:
        print('Game not found')
        raise DynamoDBException('Game not found')
    if cpu is not None and gpu is not None and game is not None:
        fps = FPS()
        cpu = dict(cpu)
        gpu = dict(gpu)
        game = dict(game)
        for key, value in cpu.items():
            fps.add_info('CPU-' + key, value)
        for key, value in gpu.items():
            fps.add_info('GPU-' + key, value)
        for key, value in game.items():
            fps.add_info('GAME-' + key, value)
        fps.add_info('Res-Width', decimal.Decimal(reswidth))
        fps.add_info('Res-Height', decimal.Decimal(resheight))
        fps.add_info('Game-Setting', gamesetting)
        fps.add_info('Ram', decimal.Decimal(ram))
        fps.add_info('id', 'prediction')
        fps.add_info('target', decimal.Decimal(0.0))
        ####Generate CSV file
        ref_date = datetime.strptime('1995-01-01', '%Y-%m-%d')
        required_col_num = 80
        label_col_num = 78
        label_col = 'target'
        string_col_num = [2, 7, 9, 10, 12, 13, 18, 23, 24, 28, 34, 36, 40, 41, 42, 43, 48, 50, 51, 54, 56, 59, 60,
                          61,
                          63, 64, 65, 66, 68, 69, 70, 72, 73, 76, 77]

        date_col_num = [17, 55, 57, 58]
        date_col_format = {17: '%b %Y', 55: '%b-%d-%Y', 57: '%b-%d-%Y', 58: '%b-%d-%Y'}

        final_fps=FPS()
        if len(file_field) == required_col_num and file_field[label_col_num] == label_col:
            for i, key in enumerate(file_field):
                word = fps.get_value(key)
                if isinstance(word, decimal.Decimal):
                    word = convert_decimal(word)
                word = str(word)
                if not word:
                    final_fps.add_info(key,0.0)
                    continue
                if len(word) <= 0:
                    final_fps.add_info(key, 0.0)
                    continue
                if i == label_col_num:
                    final_fps.add_info(key, float(word))
                elif i in string_col_num:
                    m=hashlib.md5()
                    m.update(word.encode('utf-8'))
                    num = m.hexdigest()
                    num=int(num,32)%(10**8)/2**32
                    final_fps.add_info(key, num)
                elif i in date_col_num:
                    ####handle date format
                    datetime_object = datetime.strptime(word, date_col_format.get(i))
                    feature_date = (datetime_object - ref_date).days
                    final_fps.add_info(key, float(feature_date))
                    ####handle date format
                else:
                    final_fps.add_info(key, float(word))
            keys, values = final_fps.get_all_info()
            output_df=DataFrame(np.array(values, dtype=object).reshape(1, len(values)), columns=keys,dtype='float64')
            # for i in range(10):
            #     output_df=output_df.append(DataFrame(np.array(values, dtype=object).reshape(1, len(values)), columns=keys,dtype='float64'))
            output_df = output_df[file_field]
            return output_df

def _load_data():

    dfTrain = pd.read_csv(config.TRAIN_FILE)
    dfTest = pd.read_csv(config.TEST_FILE)
    def preprocess(df):
        cols = [c for c in df.columns if c not in ["target","id"]]
        df["missing_feat"] = np.sum((df[cols] == -1).values, axis=1)
        return df

    dfTrain = preprocess(dfTrain)
    dfTest = preprocess(dfTest)
    cols = [c for c in dfTrain.columns if c not in ["target","id"]]
    cols = [c for c in cols if (not c in config.IGNORE_COLS)]

    X_train = dfTrain[cols].values
    y_train = dfTrain["target"].values

    return dfTrain, dfTest, X_train, y_train


def get_deep_fm_model(dfm_params):
    dfm_params["feature_size"] = 3024
    dfm_params["field_size"] = 74
    dfm = DeepFM(**dfm_params)
    return dfm
def prepare_dfm():
    global dfm_dnn
    global past_epoch
    dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
def predict(cpu,gpu,game,res_width,res_height,setting,ram):
    # start_time = datetime.now()
    dfTest2=interpret_predict_FPS_Data(cpu,gpu,game,res_width,res_height,setting,ram)
    cols = [c for c in dfTest2.columns if c not in ["target", "id"]]
    dfTest2["missing_feat"] = np.sum((dfTest2[cols] == -1).values, axis=1)
    global data_parser
    Xi_test, Xv_test, _ = data_parser.parse(df=dfTest2)
    ###Parse Predict Data
    global dfm_dnn
    global past_epoch
    dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
    predict_result=dfm_dnn.predict(Xi_test,Xv_test)
    # print(predict_result)
    # print('Consumed Time for Predict Data: {} second(s)'.format((datetime.now()-start_time).seconds))
    s.enter(1, 1, prepare_dfm)
    s.run()
    return predict_result
def init():
    start_time = datetime.now()
    dfTrain, dfTest, X_train, y_train = _load_data()
    # ------------------ DeepFM Model ------------------
    # params
    dfm_params = {
        "use_fm": True,
        "use_deep": True,
        "embedding_size": 16,
        "dropout_fm": [1.0, 1.0],
        "deep_layers": [2000, 2000, 1500],
        "dropout_deep": [0.5, 0.5, 0.8, 0.6],
        "deep_layers_activation": tf.nn.relu,
        "epoch": 2000,  # 500#1500
        "batch_size": 1024,
        "learning_rate": 0.001,
        "optimizer_type": "adagrad",
        "batch_norm": 1,
        "batch_norm_decay": 0.995,
        "l2_reg": 0.01,
        "verbose": True,
        "eval_metric": gini_norm,
        "random_seed": config.RANDOM_SEED,
        "loss_type": "mse"
    }
    dnn_params = dfm_params.copy()
    dnn_params["use_fm"] = False
    global dfm_dnn
    dfm_dnn= get_deep_fm_model(dnn_params)
    global past_epoch
    dfm_dnn.saver.restore(dfm_dnn.sess, "save/FixedHashing/temp" + '-' + str(past_epoch))
    ###Prepare Data Parser
    fd = FeatureDictionary(dfTrain=dfTrain, dfTest=dfTest,
                           numeric_cols=config.NUMERIC_COLS,
                           ignore_cols=config.IGNORE_COLS)
    global data_parser
    data_parser = DataParser(feat_dict=fd)
    print('Consumed Time for Prepare Model: {} second(s)'.format((datetime.now() - start_time).seconds))

    try:
        is_table_existing = hardware_table.table_status in ("CREATING", "UPDATING",
                                                   "DELETING", "ACTIVE")
    except ClientError:
        # do something here as you require
        pass
    else:
        pass

init()

import web
import json
urls = (
  '/', 'index',
    '/predict','predict_html'
)

setting_list = ["Ultra", "High", "Medium", "Low"]
paras_list=['cpu','gpu','game','resWidth','resHeight','setting','ram']
class index:
    def GET(self):
        return "Hello, world!"
class predict_html:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Headers',
                   'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
        web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        return json.dumps('OK')
    def GET(self):
        print('Preparing FPS Estismator')
        prepare_dfm()
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return json.dumps('OK')
    def POST(self):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        data = web.data()
        data=bytes(data).decode('utf-8')
        string = str(data).replace("'", '"').replace('+', ' ')
        # return web.badrequest('OMG')
        # string = str(request.data.decode('utf8')).replace("'", '"').replace('+', ' ')
        string = unquote(string)
        paras = str(string).split('&')
        print('Handling request', paras)
        if len(paras) != len(paras_list):
            print('Incorrect Parameter Length')
            raise web.badrequest("Incorrect Parameter Length")
            # return make_response(jsonify( 'Incorrect Parameter Length'), 400)
        parameters = dict()
        for para in paras:
            name, value = str(para).split('=')
            parameters.__setitem__(name, value)
        try:
            cpu = parameters.__getitem__('cpu')
            gpu =  parameters.__getitem__('gpu')
            game =  parameters.__getitem__('game')
            setting =  parameters.__getitem__('setting')
            res_height= parameters.__getitem__('resHeight')
            res_width= parameters.__getitem__('resWidth')
            ram= parameters.__getitem__('ram')
        except (KeyError):
            print('Unable to locate all Parameter')
            raise web.badrequest('Incorrect Parameter Length')
            # return make_response(jsonify('Incorrect Parameter Length'), 400)
        try:
            res_height = int(res_height)
        except (KeyError,ValueError):
            print('Unable to cast res-height')
            raise web.badrequest("Invalid data {Res-Height}")
            # return make_response(jsonify('Invalid data {Res-Height}'), 400)
        try:
            res_width = int(res_width)
        except (KeyError, ValueError):
            print('Unable to cast res-width')
            raise web.badrequest("Invalid data {Res-Width}")
            # return make_response(jsonify('Invalid data {Res-Width}'), 400)
        try:
            ram = int(ram)
        except (KeyError, ValueError):
            print('Unable to cast ram')
            raise web.badrequest("Invalid data {Ram}")
            # return make_response(jsonify('Invalid data {Ram}'), 400)

        if setting not in setting_list:
            print('Invalid Setting,could only be ' + str(setting_list))
            raise web.badrequest("Invalid data {Setting}")
            # return "BAD"
            # return make_response(jsonify('Invalid data {Setting}'), 400)
        try:
            result = predict(cpu, gpu,game,
                          res_width, res_height, setting, ram)
        except DynamoDBException:
            raise web.internalerror("Data Not Found")
            # return make_response(jsonify('Data Not Found'), 404)
        output = result[0]
        dict_return=dict({'result':str(output)})
        return json.dumps(dict_return)
        # # # return web.ok(output)
        # return output
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()