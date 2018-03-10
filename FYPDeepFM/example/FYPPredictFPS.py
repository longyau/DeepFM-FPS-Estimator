import boto3
import os
from boto3.dynamodb.conditions import Key, Attr,AttributeBase
from botocore.exceptions import ClientError
import decimal
from datetime import datetime
dynamodb = boto3.resource('dynamodb')
hardware_table = dynamodb.Table('FYP_Hardware')
class FPS(object):
    def add_info(self, name,value):
        try:
            name = name[:name.index('(')]
        except ValueError:
            pass
        self.__setattr__(name, value)
    def get_detail(self):
        return repr(self.__dict__)
    def __iter__(self):
        for key,value in self.__dict__.items():
            yield key, value
    def get_all_info(self):
        keys=[]
        values=[]
        for key,value in self.__dict__.items():
            keys.append(key)
            values.append(value)
        return keys,values
    def get_value(self,name:str):
        try:
            output=self.__getattribute__(name)
            if output is not None:
                return output
            else:
                return ''
        except AttributeError:
            return ''


def convert_decimal(o):
    if isinstance(o, decimal.Decimal):
        if o % 1 > 0:
            return float(o)
        else:
            return int(o)


def getCPUData(cpu_name:str):
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
def getGPUData(gpu_name:str):
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


def getGameData(game_name:str):
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
def combineInformation(cpu_name:str,gpu_name:str,game_name:str,reswidth:int,resheight:int,gamesetting:str,ram:int):
    predict_file=open("predict/predict.txt", 'w', encoding='utf-8')
    predict_csv = open("predict/predict.csv", 'w', encoding='utf-8')
    file_field_string="CPU-Score	CPU-Cache L1	CPU-Socket	CPU-Cache L3	CPU-Cache L2	CPU-Samples	CPU-Process	CPU-Brand	CPU-Cores	CPU-Type	CPU-URL	CPU-Clock	CPU-Part Number	CPU-Codename	CPU-Multi	CPU-Price	CPU-TDP	CPU-Released	CPU-Name	GPU-L2 Cache	GPU-Shader Processing Units	GPU-Process	GPU-Samples	GPU-Website	GPU-Brand	GPU-Direct X	GPU-Release Price	GPU-TMUs	GPU-PSU	GPU-ROPs	GPU-Max Power	GPU-Texture Rate	GPU-Memory	GPU-GD RATING	GPU-BenchmarkURL	GPU-Core Speed	GPU-Name	GPU-Pixel Rate	GPU-Memory Bandwidth	GPU-Shader	GPU-Name2	GPU-Power Connector	GPU-Type	GPU-Architecture	GPU-Benchmark	GPU-Memory Speed	GPU-Open GL	GPU-Memory Bus	GPU-Memory Type	GAME-Rec-DX	GAME-Website	GAME-Theme	GAME-Min-DX	GAME-Rec-Ram	GAME-Min-CPU0	GAME-Release Date2	GAME-Min-CPU1	GAME-Release Date0	GAME-Release Date1	GAME-Min-GPU1	GAME-Min-GPU0	GAME-Name	GAME-Min-VRam	GAME-Rec-CPU1	GAME-Min-OS	GAME-Rec-CPU0	GAME-Rec-GPU1	GAME-Min-Ram	GAME-Rec-GPU0	GAME-Type	GAME-Rec-OS	GAME-Rec-VRam	GAME-Genre1	GAME-Genre0	Res-Height	Res-Width	FPS_Id	Game-Setting	FPS	Ram"
    file_field=file_field_string.split('\t')
    print(file_field)
    cpu=getCPUData(cpu_name)
    gpu=getGPUData(gpu_name)
    game=getGameData(game_name)
    if cpu is not None and gpu is not None and game is not None:
        fps = FPS()
        cpu = dict(cpu)
        gpu = dict(gpu)
        game = dict(game)
        print('CPU')
        for key, value in cpu.items():

            if isinstance(value, decimal.Decimal):
                print('Key{}:{}'.format(key,value))
            fps.add_info('CPU-' + key, value)
        for key, value in gpu.items():
            fps.add_info('GPU-' + key, value)
        for key, value in game.items():
            fps.add_info('GAME-' + key, value)
        fps.add_info('Res-Width',decimal.Decimal(reswidth))
        fps.add_info('Res-Height',decimal.Decimal(resheight))
        fps.add_info('Game-Setting',gamesetting)
        fps.add_info('Ram',decimal.Decimal(ram))
        fps.add_info('FPS_Id','prediction')
        fps.add_info('FPS',decimal.Decimal(0))
        print('Object')
        for field in file_field:
            predict_file.write(field + '\t')
        predict_file.write('\n')
        for field in file_field:
            field_value = fps.get_value(field)
            if isinstance(field_value, decimal.Decimal):
                print('Field{0}:{1}'.format(field,field_value))
                field_value = convert_decimal(field_value)
            predict_file.write(str(field_value) + '\t')
        predict_file.write('\n')
        predict_file.close()
        ####Generate CSV file
        ref_date = datetime.strptime('1995-01-01', '%Y-%m-%d')
        required_col_num = 80
        label_col_num = 78
        label_col = 'FPS'
        string_col_num = [2, 7, 9, 10, 12, 13, 18, 23, 24, 28, 34, 36, 40, 41, 42, 43, 48, 50, 51, 54, 56, 59, 60, 61,
                          63, 64, 65, 66, 68, 69, 70, 72, 73, 76, 77]
        date_col_num = [17, 55, 57, 58]
        date_col_format = {17: '%b %Y', 55: '%b-%d-%Y', 57: '%b-%d-%Y', 58: '%b-%d-%Y'}

        if len(file_field)==required_col_num and file_field[label_col_num]== label_col:
            for i, word in enumerate(file_field):
                if i != 0: predict_csv.write(',')
                if word=='FPS':word='target'
                if word=='FPS_Id':word='id'
                predict_csv.write(word)
            predict_csv.write('\n')
            for i, key in enumerate(file_field):
                word=fps.get_value(key)
                if isinstance(word, decimal.Decimal):
                    word = convert_decimal(word)
                word=str(word)
                if i != 0: predict_csv.write(',')
                if not word:
                    # cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    predict_csv.write('0')
                    continue
                if len(word) <= 0:
                    # cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    predict_csv.write('0')
                    continue
                if i == label_col_num:
                    # label=float(word)
                    predict_csv.write(str(float(word)))
                elif i in string_col_num:
                    num = (hash(word) + 2.0 ** 31) / 2 ** 32
                    predict_csv.write(str(num))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(num)])
                elif i in date_col_num:
                    ####handle date format
                    datetime_object = datetime.strptime(word, date_col_format.get(i))
                    feature_date = (datetime_object - ref_date).days
                    predict_csv.write(str(float(feature_date)))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(feature_date)])
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, word])
                ####handle date format
                else:
                    predict_csv.write(str(float(word)))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(word)])
                    # print(cur_feature_list)
                    # features.append(cur_feature_list)
                    # labels.append(label)
            predict_csv.write('\n')
            for i in range(839):
                for field_i,_ in enumerate(file_field):
                    if field_i != 0: predict_csv.write(',')
                    predict_csv.write('0.0')
                predict_csv.write('\n')
            predict_csv.close()

combineInformation('Core i3 530','GeForce GT 610','Kingdom Come: Deliverance',1024,720,'Low',4)
# import hashlib
# m=hashlib.md5()
# text='Ultra'
#
# m.update(text.encode('utf-8'))
# num=m.hexdigest()
# num=int(num, 32) % (10 ** 8)/ 2 ** 32
# # num = (hash('Ultra'))
# print(num)
# m=hashlib.md5()
# text='Hgih'
#
# m.update(text.encode('utf-8'))
# num=m.hexdigest()
# num=int(num, 32) % (10 ** 8)/ 2 ** 32
# # num = (hash('Ultra'))
# print(num)