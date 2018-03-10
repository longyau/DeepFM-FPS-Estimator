import boto3
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FYP_Hardware')
subsituition=[['\n',''],['<br>',' '],['&amp;','']]
# handling=[['Name','str','Name'],['Process','int','Process(nm)'],['TMUs','int','TMUs'],['Texture Rate','decimal','Texture Rate(GTexel/s)'],['ROPs','decimal','ROPs'],['Pixel Rate','decimal','Pixel Rate(GPixels)'],['Shader Processing Units(Cuda Cores) ','int','Shader Processing Units(Cuda Cores)'],['Direct X','decimal','Direct X'],
handling_exception=['Website','Name','Architecture','Memory Type','PSU','Power Connector']
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

class GPU(object):
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

def get_grapped_gpu(filename:str,path:str):
    import decimal
    import time
    output=GPU()
    skips=False
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as grapped_file:
        # print(grapped_file.name)
        lines=grapped_file.readlines()
        for line in lines:
            try:
                cols=line.split('\t')
                skips=False
                for index in range(len(cols)):
                    for from_pattern, to_pattern in subsituition:
                        cols[index]=cols[index].replace(from_pattern, to_pattern)
                for exception in handling_exception:
                    if cols[0]==exception:
                        skips=True
                        break
                if not skips:
                    starting_num_index=-1
                    last_num_index=len(cols[1])-1
                    for index in range(len(cols[1])):
                        if (cols[1][index]>='0' and cols[1][index]<='9') or cols[1][index]=='.':
                            if starting_num_index == -1:
                                starting_num_index = index
                            last_num_index=index
                        elif starting_num_index!=-1:
                            break
                    if starting_num_index==-1:
                        starting_num_index=0
                    sub_title=cols[1][last_num_index+1:len(cols[1])].replace(' ','')
                    if len(sub_title)>0:
                        cols[0]+="({0})".format(sub_title)
                    try:
                        cols[1]=decimal.Decimal(cols[1][starting_num_index:last_num_index+1])
                    except decimal.InvalidOperation:
                        if len(cols[1]) == 0:
                            cols[1] = decimal.Decimal(0.0)
                        else:
                            print('Error{}:{}'.format(cols[0],cols[1]))
                            time.sleep(100)
                # value=str(value).replace('\n','')
                output.add_info(cols[0],cols[1])
                if str(cols[1])==' ':
                    print(line + 'have error')
            except ValueError:
                print(line+'have error')
                time.sleep(100)
    return output

def readData(in_file_path:str='..\..\FYPScrapper\GPUSpecScrapper\grapped\gpuSpec'):
    file_cnt = 0
    # game_array = []
    for folder in os.listdir(in_file_path):
        # try:
        #     folder_name = int(folder)
        #     if folder_name > 2018 or folder_name < 1999:
        #         continue
        # except AttributeError:
        #     continue
        with table.batch_writer() as batch:
            exact_path = in_file_path + '\\' + folder
            for filename in os.listdir(exact_path):
                file_cnt += 1
                try:
                    assert filename.endswith('.txt')
                    # updateModel(filename,exact_path)
                    # checkBestSuitMark(filename,exact_path,gpu_name_list)


                    gpu=get_grapped_gpu(filename,exact_path)
                    gpu.add_info('Type','GPU-Config')
                    print(gpu.get_detail())
                    batch.put_item(
                       Item=gpu.__dict__
                    )



                    # game_array.append({folder: filename[:-4]})
                    # game_array.append(gpu)
                except AssertionError:
                    continue
    # return game_array, file_cnt
    print(file_cnt)
readData()