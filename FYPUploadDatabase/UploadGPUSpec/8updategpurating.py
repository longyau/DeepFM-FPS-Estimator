import boto3
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FYP_Hardware')
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
###declare a python object to store all GPU benchmark data
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


###read the CSV file and get a list of GPU benchmark data
def readCSVFile():
    output=[]
    import csv
    with open('../../FYPScrapper/GPUSpecScrapper/res/GPU_UserBenchmarks.csv', 'r', encoding='utf8') as orgData:
        reader = csv.DictReader(orgData)
        for index, row in enumerate(reader):
            gpu = GPU()
            for key, itm in row.items():
                gpu.add_info(key, itm)
            output.append(gpu)
    return output


###Update benchmark data on DynamoDB based on the benchmark data list
def updateDB(data_name:str,rating_name:str,rating_list):
    import decimal
    for rating_item in rating_list:
        # print('Finding:{},{}'.format(rating_name,rating_item.Model))
        if rating_item.Model==rating_name:
            # print('Found:'.format(rating_item.Model))
            # print(rating_item.Model)
            response = table.update_item(
                Key={
                    'Type': 'GPU-Config',
                    'Name': data_name
                },
                UpdateExpression="set Name2 = :n2, Brand=:b, Benchmark=:bench, Samples=:sample, BenchmarkURL=:url",
                ExpressionAttributeValues={
                    ':n2': rating_item.Model,
                    ':b': rating_item.Brand,
                    ':bench':decimal.Decimal(rating_item.Benchmark),
                    ':sample':decimal.Decimal(rating_item.Samples),
                    ':url':rating_item.URL,
                },
                ReturnValues="UPDATED_NEW"
            )
            print('{} updated'.format(repr(response)))


###Read all the paired-data in "match.txt" to trigger "updateDB" function
def readData(in_file_path:str='..\..\FYPScrapper\GPUSpecScrapper\matching.txt'):
    file_cnt = 0
    gpu_rating_list=readCSVFile()
    with open(in_file_path, 'r', encoding='utf8') as matching_file:
        lines=matching_file.readlines()
        for line in lines:
            if len(line) < 1: break
            cols = line.replace('\n','').split('\t')
            # print('cols[0]:{},cols[1]:{}'.format(cols[0],cols[1]))
            updateDB(cols[0],cols[1],gpu_rating_list)
    print(file_cnt)
readData()