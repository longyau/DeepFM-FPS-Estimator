import boto3
import os
from boto3.dynamodb.conditions import Key, Attr,AttributeBase
from botocore.exceptions import ClientError
import decimal
dynamodb = boto3.resource('dynamodb')
fps_table = dynamodb.Table('FYP_FPSRecord')
hardware_table = dynamodb.Table('FYP_Hardware')
# upload_table = dynamodb.Table('FYP_FPS_Full_Record')
subsituition=[['\n',''],['<br>',' '],['&amp;',''],['...','']]
# handling=[['Name','str','Name'],['Process','int','Process(nm)'],['TMUs','int','TMUs'],['Texture Rate','decimal','Texture Rate(GTexel/s)'],['ROPs','decimal','ROPs'],['Pixel Rate','decimal','Pixel Rate(GPixels)'],['Shader Processing Units(Cuda Cores) ','int','Shader Processing Units(Cuda Cores)'],['Direct X','decimal','Direct X'],
convert_to_decimal=['Res-Width','Res-Height','FPS','Ram']
###declare a python object to store all information related to the FPS
class FPS(object):
    def add_info(self, name:str,value):
        try:
            name=name[:name.index('(')]
        except ValueError:
            pass
        self.__setattr__(name,value)
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

# def write_fps_to_file(fps:FPS,output_file):
#     keys,values=fps.get_all_info()
#     for i in enumerate(keys):
#         output_file.write()
###python function to convert decimal data to float or int
def convert_decimal(o):
    if isinstance(o, decimal.Decimal):
        if o % 1 > 0:
            return float(o)
        else:
            return int(o)


###Make a query on DynamoDB for the CPU Data
def query_cpu_info(cpu_name:str,tail_name:str=''):
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
        # print(json.dumps(item, indent=4, cls=DecimalEncoder))
    except ClientError as e:
        print(e.response['Error']['Message'])
    except KeyError:
        if tail_name == '':
            try:
                new_name = cpu_name[:cpu_name.rindex(' ')]
                tail_name = cpu_name[cpu_name.rindex(' ') :]
                return query_cpu_info(new_name, tail_name)
            except ValueError:
                return

        elif tail_name=='last_try':
            return
        else:
            original_name = cpu_name + tail_name
            try:
                cols = str(original_name).split(' ')
                max_col = cols[0]
                for col in cols:
                    # print('cols{}:sum{}'.format(col,sum(c.isdigit() for c in col)))
                    if sum(c.isdigit() for c in col) >= sum(c.isdigit() for c in max_col):
                        max_col = col
                # print('MaxCol is {}'.format(max_col))
                cpu_name=original_name[:original_name.index(max_col)+len(max_col)]
                # print('cpu_name is {}'.format(cpu_name))
                tail_name='last_try'
                return query_cpu_info(cpu_name,tail_name)
            except ValueError:
                return
            ####scannning
            #
            # fe = Key('Type').eq('CPU-Config') and Attr('Name').contains(max_col)
            # try:
            #     response = hardware_table.scan(
            #     FilterExpression=fe,
            #     )
            # except ClientError as e:
            #     print(e.response['Error']['Message'])
            #     query_cpu_info(cpu_name, tail_name)
            # for i,item in enumerate(response['Items']):
            #     # print("Finally..GetItem succeeded:{}".format(item))
            #     if i==0: return item

                ####scannning

    # response = hardware_table.query(
    #     KeyConditionExpression=Key('Type').eq('CPU-Config')
    #
    # )

###Make a query on DynamoDB for the GPU Data
def query_gpu_info(gpu_name:str,tail_name:str=''):

    try:
        response = hardware_table.get_item(
            Key={
                'Type': 'GPU-Config',
                'Name': gpu_name
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        try:
            item = response['Item']
            # print("GetItem succeeded:{}".format(item))
            return item
        except KeyError:
            if tail_name == '':
                try:
                    new_name = gpu_name[:gpu_name.rindex(' ')]
                    tail_name = gpu_name[gpu_name.rindex(' '):]
                    return query_gpu_info(new_name, tail_name)
                except ValueError:
                    return


###Make a query on DynamoDB for the Game Data
def query_game_info(game_name: str):

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



###run thorugh all FPS records on DynamoDB
###get all the related CPU,  GPU and Game Data
###if any of the data is missing, move it into dopped.txt
###20% of the complete record is test data
###80% of the complete record is train data
def readData():
    fps_cnt = folder_cnt=0
    train_file_cnt=test_file_cnt=dropped_file_cnt=0
    prev_game_name=''
    prev_game=None
    # response = fps_table.query(
    #     KeyConditionExpression=Key('Game_Name').eq('For Honor') & Key('FPS_Id').begins_with('23270')
    # )
    # retry=0
    # while retry < 5:
    try:
        response = fps_table.scan()
        # break
    except ClientError as e:
        print(e.response['Error']['Message'])
            # retry+=1

    train_file=open('train.txt','w',encoding='utf-8')
    test_file=open('test.txt','w',encoding='utf-8')
    dropped_file=open('dropped.txt','w',encoding='utf-8')
    # test_file_field = train_file_field = []
    file_field=[]
    for i in response['Items']:
        if fps_cnt%1000==0:
            folder_cnt+=1
            train_file.close()
            test_file.close()
            dropped_file.close()
            train_file = open('train-' + str(folder_cnt) + '.txt', 'w', encoding='utf-8')
            test_file = open('test-' + str(folder_cnt) + '.txt', 'w', encoding='utf-8')
            dropped_file = open('dropped-' + str(folder_cnt) + '.txt', 'w', encoding='utf-8')
        item=dict(i)
        cpu_name=item.get('CPU')
        cpu_name=str(cpu_name).replace('Ryzen R','Ryzen ')
        cpu_name = str(cpu_name).replace('Pentium Dual Core', 'Pentium')
        cpu=query_cpu_info(cpu_name)
        gpu_name=item.get('GPU')
        gpu=query_gpu_info(gpu_name)
        game_name=item.get('Game_Name')
        if game_name!= prev_game_name:
            prev_game_name=game_name
            prev_game=query_game_info(game_name)
        game=prev_game
        if cpu is not None and gpu is not None and game is not None:
            fps=FPS()
            cpu = dict(cpu)
            gpu = dict(gpu)
            game=dict(game)
            for key,value in cpu.items():
                fps.add_info('CPU-'+key,value)
            for key,value in gpu.items():
                fps.add_info('GPU-'+key,value)
            for key, value in game.items():
                fps.add_info('GAME-' + key, value)
            for key, value in item.items():
                if key=='CPU' or key=='GPU' or key=='Game_Name':
                    continue
                else:
                    fps.add_info(key, value)
            import random
            # number=2
            number=random.randint(1,10)
            print('CPU-Name:{},GPU-Name:{},Game-Name:{} found record'.format(fps.get_value('CPU-Name'),fps.get_value('GPU-Name'),fps.get_value('GAME-Name')))
            if test_file_cnt==0 and train_file_cnt==0:
                keys, values = fps.get_all_info()
                for key in keys:
                    file_field.append(key)
            if number > 8:
                if test_file_cnt==0:
                    for field in file_field:
                        test_file.write(field + '\t')
                    test_file.write('\n')
                for field in file_field:
                    field_value=fps.get_value(field)
                    if isinstance(field_value,decimal.Decimal):
                        field_value=convert_decimal(field_value)
                    test_file.write(str(field_value)+'\t')
                test_file.write('\n')
                test_file_cnt+=1
            else:
                if train_file_cnt==0:
                    for field in file_field:
                        train_file.write(field + '\t')
                    train_file.write('\n')
                for field in file_field:
                    field_value=fps.get_value(field)
                    if isinstance(field_value,decimal.Decimal):
                        field_value=convert_decimal(field_value)
                    train_file.write(str(field_value)+'\t')
                train_file.write('\n')
                train_file_cnt+=1
        else:
            dropped_file.write('{}\t{}\t{}\t\n'.format(cpu_name,gpu_name,game_name))
        # print('Next.....CPU:{},GPU:{},Game:{}'.format(cpu_name,gpu_name,game_name))
        fps_cnt+=1
        # print(json.dumps(i, cls=DecimalEncoder))
    train_file.close()
    test_file.close()
    dropped_file.close()
    print('FPS Count:{},Train Data Count:{},Test Data Count:{}'.format(fps_cnt,train_file_cnt,test_file_cnt))
readData()