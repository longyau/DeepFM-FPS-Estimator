import boto3
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FYP_Hardware')
subsituition=[['\n',''],['<br>',' '],['&amp;',''],['&nbsp;',' '],['nbsp;',' ']]
skipped_attribute_list=['Rank','Name']
change_attribute_name={'Model':'Name'}
# handling=[['Name','str','Name'],['Process','int','Process(nm)'],['TMUs','int','TMUs'],['Texture Rate','decimal','Texture Rate(GTexel/s)'],['ROPs','decimal','ROPs'],['Pixel Rate','decimal','Pixel Rate(GPixels)'],['Shader Processing Units(Cuda Cores) ','int','Shader Processing Units(Cuda Cores)'],['Direct X','decimal','Direct X'],
handling_exception=['Type','Part Number','Brand','Model','URL','Name','Codename','Socket','Released']
special_deciaml=['Cores','Cache L1/L2/L3']
# table.put_item(
#    Item={
#         'Type': 'GPU-Test',
#         'Name': 'Dummy',
#         'score': int(1),
#     }
# )
# response = table.get_item(
#     Key={
#         'Type': 'GPU-Test',
#         'Name': 'Dummy'
#     }
# )
# item = response['Item']
# print(item)
class MyException(Exception):
    pass


class CPU(object):
    def add_info(self, name,value):
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


def convert_to_decimal(column_name:str,column_value:str):
    import decimal
    import time
    starting_num_index = -1
    last_num_index = len(column_value) - 1
    for index_of_col in range(len(column_value)):
        if (column_value[index_of_col] >= '0' and column_value[index_of_col] <= '9') or column_value[index_of_col] == '.':
            if starting_num_index == -1:
                starting_num_index = index_of_col
            last_num_index = index_of_col
        elif starting_num_index != -1:
            break
    if starting_num_index == -1:
        starting_num_index = 0
    sub_title = column_value[last_num_index + 1:len(column_value)].replace(' ', '')
    if len(sub_title) > 0:
        column_name += "({0})".format(sub_title)
    try:
        column_value = decimal.Decimal(column_value[starting_num_index:last_num_index + 1])
    except decimal.InvalidOperation:
        if len(column_value) == 0:
            column_value = decimal.Decimal(0.0)
        else:
            print('Error{}:{}'.format(column_name, column_value))
            time.sleep(100)
    return column_name,column_value

def get_grapped_cpu_list(filename:str,path:str):
    import decimal
    import time
    output=list()
    skips=False
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as grapped_file:
        ###get first line
        line=grapped_file.readline()
        if line.startswith('\ufeff'): line=line[1:]
        if line.endswith('\t\n'):line=line[:-(len('\t\n'))]
        attribute_name_list = line.split('\t')
        ###get first line
        while True:
            line=grapped_file.readline()
        ###break loop if file is ended
            if not line:
                break
        ###break loop if file is ended
            try:
                if line.startswith('\ufeff'): line = line[1:]
                if line.endswith('\t\n'):line = line[:-(len('\t\n'))]
                cpu = CPU()
                cols=line.split('\t')
                for index in range(len(cols)):
                    skips = False
                    attribute_name=attribute_name_list[index]
                    if attribute_name in skipped_attribute_list:
                        continue
                    if change_attribute_name.get(attribute_name) != None:
                        attribute_name = change_attribute_name.get(attribute_name)
                    if attribute_name in handling_exception:
                        skips = True
                    for from_pattern, to_pattern in subsituition:
                        cols[index]=cols[index].replace(from_pattern, to_pattern)
                    if not skips:
                        if not attribute_name in special_deciaml:
                            try:
                                attribute_name.index('Cache')
                                print('found cache,{}'.format(repr(attribute_name)))
                            except:
                                pass
                            attribute_name,cols[index]=convert_to_decimal(attribute_name,cols[index])
                        else:
                            if attribute_name=='Cores':
                                ### Seperate into Core and Threads
                                try:
                                    core_num,thread_num=cols[index].split('/')
                                    attribute_name, thread_decimal = convert_to_decimal('Threads', thread_num)
                                    cpu.add_info(attribute_name,thread_decimal)
                                    attribute_name, cols[index] = convert_to_decimal('Cores', core_num)
                                except ValueError:
                                    attribute_name, cols[index] = convert_to_decimal('Cores', core_num)
                                ### Seperate into Core and Threads
                            elif attribute_name=='Cache L1/L2/L3':
                                ###seperate into l1,l2,l3
                                try:
                                    l1_num,l2_num,l3_num=cols[index].split('/')
                                    attribute_name, l2_decimal = convert_to_decimal('Cache L2', l2_num)
                                    cpu.add_info(attribute_name, l2_decimal)
                                    attribute_name, l3_decimal = convert_to_decimal('Cache L3', l3_num)
                                    cpu.add_info(attribute_name, l3_decimal)
                                    attribute_name, cols[index] = convert_to_decimal('Cache L1', l1_num)
                                except ValueError:
                                    attribute_name, cols[index] = convert_to_decimal('Cache L1', core_num)
                                ###seperate into l1,l2,l3
                            else:
                                raise MyException('Action of attribute Name {} in (special_decimal) list is not defined'.format(attribute_name))
                    if not(type(cols[index]) is str and len(cols[index])==0):
                        cpu.add_info(attribute_name,cols[index])
                try:
                    cpu.Codename
                    output.append(cpu)
                except AttributeError:
                    pass
            except ValueError:
                print(line+'have error')
                time.sleep(100)
            except MyException as e:
                print(e.args[0])

    return output

def readData(in_file_path:str='..\..\FYPScrapper\CPUSpecScrapper\\res'):
    filename='CPU_Data.txt'
    try:
        assert filename.endswith('.txt')
        # updateModel(filename,exact_path)
        # checkBestSuitMark(filename,exact_path,gpu_name_list)
        cpu_list=get_grapped_cpu_list(filename,in_file_path)
        cnt=0
        with table.batch_writer() as batch:
            for cpu in cpu_list:
                cpu.add_info('Type','CPU-Config')
                print(cpu.get_detail())
                batch.put_item(
                   Item=cpu.__dict__
                )
                cnt+=1
        print('uploaded total:{}'.format(cnt))
    except AssertionError:
        print('omg')
readData()