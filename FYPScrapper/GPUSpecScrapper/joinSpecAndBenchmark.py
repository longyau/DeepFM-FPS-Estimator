import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common import exceptions
import urllib.parse as urllib
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
    output=GPU()
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as grapped_file:
        # print(grapped_file.name)
        lines=grapped_file.readlines()
        for line in lines:
            try:
                cols=line.split('\t')
                cols=[str(col).replace('\n','') for col in cols]
                # value=str(value).replace('\n','')
                output.add_info(cols[0],cols[1])
                if str(cols[1])==' ':
                    print(line + 'have error')
            except ValueError:
                print(line+'have error')
                import time
                time.sleep(100)
    return output


def checkBestSuitMark(filename:str,path:str,gpu_name_list:[]):
    import difflib
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as grapped_file:
        print(grapped_file.name)
        grapped_file.readline()
        name_line=grapped_file.readline()
        chkmodel,name=name_line.split('\t')
        if chkmodel!="Name":
            return False
        # gpu_name_list=[str(gpu.Model) for gpu in gpu_list]
        rseult=difflib.get_close_matches(name,gpu_name_list)
        print('Name:{},Match{}'.format(name,rseult))


def readData(in_file_path:str='grapped\gpuSpec'):
    file_cnt = 0
    game_array = []
    for folder in os.listdir(in_file_path):
        # try:
        #     folder_name = int(folder)
        #     if folder_name > 2018 or folder_name < 1999:
        #         continue
        # except AttributeError:
        #     continue
        exact_path = in_file_path + '\\' + folder
        for filename in os.listdir(exact_path):
            file_cnt += 1
            try:
                assert filename.endswith('.txt')
                # updateModel(filename,exact_path)
                # checkBestSuitMark(filename,exact_path,gpu_name_list)
                gpu=get_grapped_gpu(filename,exact_path)
                # print(gpu.get_detail())
                # game_array.append({folder: filename[:-4]})
                game_array.append(gpu)
            except AssertionError:
                continue
    return game_array, file_cnt


def updateModel(filename:str,path:str):
    no_model_name=True
    try:
        assert filename.endswith('.txt')
        int(filename[:-4])
        ##get website
    except ValueError:
        no_model_name=False
    except AssertionError:
        return False
    with open(os.path.relpath(path+'/'+filename), 'r', encoding='utf8') as output_file:
        print(output_file.name)
        lines=output_file.readlines()
        print(lines)
        if no_model_name:
            print(lines[0])
            _,link=lines[0].split('\t')
            link = str(link)
            link = urllib.unquote(link)
            model_name = link[link.index('graphics=') + len('graphics='):]
            model_name=str(model_name).replace('\n','')
        else:
            model_name = filename[:-4]
        with open(os.path.relpath(path + '/' + filename), 'w', encoding='utf8') as output_file:
            output_file.write(lines[0])
            output_file.write('Name\t'+model_name+'\n')
            for i in range(1,len(lines)):
                try:
                    lines[i].index('\t')
                    output_file.write(lines[i])
                except ValueError:
                    if lines[i].endswith('\n'):
                        output_file.write(lines[i][:-(len('\n'))])
            # output_file.writelines(lines[1:])

def readCSVFile():
    output=[]
    import csv
    with open('res/GPU_UserBenchmarks.csv', 'r', encoding='utf8') as orgData:
        reader = csv.DictReader(orgData)
        for index, row in enumerate(reader):
            gpu = GPU()
            for key, itm in row.items():
                gpu.add_info(key, itm)
            output.append(gpu)
    return output

def main():
    csv_gpu_list=readCSVFile()
    grapped_arr,cnt=readData()
    grapped_gpu_name_list=[]
    for gpu in grapped_arr:
        grapped_gpu_name_list.append(gpu.Name)
    # gpu_name_list = [gpu.Model for gpu in gpu_list]
    # import difflib
    from fuzzywuzzy import fuzz
    remove_strings=["Radeon","GeForce"]
    output_file=open('matching.txt','w', encoding='utf8')
    for grapped_name in grapped_gpu_name_list:
        modified_name=grapped_name
        for remove_string in remove_strings:
            modified_name=str(modified_name).replace(remove_string,'')
        # gpu_name_list=[str(gpu.Model) for gpu in gpu_list]
        best=""
        score=0
        check_col = ""
        cols = str(modified_name).split(' ')
        for col in cols:
            # print('cols{}:sum{}'.format(col,sum(c.isdigit() for c in col)))
            if sum(c.isdigit() for c in col) > 2:
                check_col = col
                break
        for gpu in csv_gpu_list:
            if check_col!="":
                try:
                    str(gpu.Model).index(check_col)
                except ValueError:
                    continue
            tmp_score = fuzz.ratio(gpu.Model, modified_name)
            if tmp_score >=score:
                best=gpu.Model
                score=tmp_score
        # rseult = difflib.get_close_matches(gpu.Model, grapped_gpu_name_list,n=1)
        if score>0:
            output_file.write('{}\t{}\n'.format(grapped_name,best))
            print('Name:{},Match{},Score{}'.format(grapped_name, best,score))
    output_file.close()
    print(cnt)


main()

