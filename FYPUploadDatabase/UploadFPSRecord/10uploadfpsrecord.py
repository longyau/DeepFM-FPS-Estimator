import boto3
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FYP_FPSRecord')
subsituition=[['\n',''],['<br>',' '],['&amp;',''],['...','']]
# handling=[['Name','str','Name'],['Process','int','Process(nm)'],['TMUs','int','TMUs'],['Texture Rate','decimal','Texture Rate(GTexel/s)'],['ROPs','decimal','ROPs'],['Pixel Rate','decimal','Pixel Rate(GPixels)'],['Shader Processing Units(Cuda Cores) ','int','Shader Processing Units(Cuda Cores)'],['Direct X','decimal','Direct X'],
convert_to_decimal=['Res-Width','Res-Height','FPS','Ram']
###declare a python object to store all FPS Data
class FPS(object):
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

###Convert the scrapped FPS file into python object
def get_grapped_fps(filename:str,path:str):
    import decimal
    import time

    output=list()
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as grapped_file:
        game_name=None
        game_id=filename[:-(len('.txt'))]
        another_file_name='{0}/../../gameInfo/{1}/{2}'.format(path,path[path.rindex('\\')+len('\\'):],filename)
        with open(os.path.relpath(another_file_name),'r', encoding='utf-8') as another_file:
            another_file.readline()
            line = another_file.readline()
            try:
                attribute_name, attribute=line.replace('\n','').split('\t')
                if attribute_name == 'Name': game_name = attribute
            except ValueError:
                return output
        fps=None
        while True:
            line=grapped_file.readline()
            if not line:
                if fps is not None:
                    output.append(fps)
                break
            try:
                cols=line.split('\t')
                if len(cols)==1:
                    try:
                        int(cols[0])
                        if fps!=FPS():
                            output.append(fps)
                        fps=FPS()
                        fps.add_info('FPS_Id',game_id+'-'+cols[0][:-len('\n')])
                        if game_name is not None: fps.add_info('Game_Name',game_name)
                        continue
                    except ValueError:
                        raise
                to_decimal=False
                for index in range(len(cols)):
                    for from_pattern, to_pattern in subsituition:
                        cols[index]=cols[index].replace(from_pattern, to_pattern)
                if cols[0] in convert_to_decimal:to_decimal=True
                if to_decimal:
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
                if not (type(cols[1]) is str and len(cols[1]) == 0):
                    fps.add_info(cols[0], cols[1])
                if str(cols[1])==' ':
                    print(line + 'have error')
            except ValueError:
                print(line+'have error')
                time.sleep(100)
    return output


###Loop through each "txt" file in "FYPScrapper" and upload to DynamoDB
def readData(in_file_path:str='..\..\FYPScrapper\FPS&GameSpecScrapper\grapped\FPSRecord'):
    file_cnt=fps_cnt = 0
    # game_array = []
    # for folder in os.listdir(in_file_path):
    for folder in range(2015,2018,1):
        # try:
        #     folder_name = int(folder)
        #     if folder_name > 2018 or folder_name < 1999:
        #         continue
        # except AttributeError:
        #     continue
        with table.batch_writer() as batch:
            exact_path = in_file_path + '\\' + str(folder)
            for filename in os.listdir(exact_path):
                file_cnt += 1
                try:
                    assert filename.endswith('.txt')
                    # updateModel(filename,exact_path)
                    # checkBestSuitMark(filename,exact_path,gpu_name_list)


                    fps_records=get_grapped_fps(filename,exact_path)
                    for fps_record in fps_records:
                        if fps_record is None:continue
                        # print(fps_record)
                        print(fps_record.get_detail())
                        fps_cnt+=1
                        batch.put_item(
                           Item=fps_record.__dict__
                        )



                    # game_array.append({folder: filename[:-4]})
                    # game_array.append(gpu)
                except AssertionError:
                    continue
    # return game_array, file_cnt
    print(file_cnt)
    print('FPS Count:{}'.format(fps_cnt))
readData()