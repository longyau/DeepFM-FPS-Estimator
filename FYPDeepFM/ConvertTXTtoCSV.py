from datetime import datetime
import hashlib
def load_data_from_file_batching(in_file,out_file):
    ref_date=datetime.strptime('1995-01-01','%Y-%m-%d')
    # labels = []
    # features = []
    cnt = 0
    required_col_num=80
    label_col_num=78
    label_col='FPS'
    string_col_num=[2,7,9,10,12,13,18,23,24,28,34,36,40,41,42,43,48,50,51,54,56,59,60,61,63,64,65,66,68,69,70,72,73,76,77]
    date_col_num=[17,55,57,58]
    date_col_format={17:'%b %Y',55:'%b-%d-%Y',57:'%b-%d-%Y',58:'%b-%d-%Y'}
    write_file=open(out_file,'w',encoding='utf-8')
    with open(in_file, 'r',encoding='utf-8') as rd:
        # rd.readline()
        while True:
            line = rd.readline()
            if not line:
                break
            cnt += 1
            line=line.replace(',','')
            if '#' in line:
                punc_idx = line.index('#')
            elif '\t\n' in line:
                punc_idx = line.index('\t\n')
            elif '\n' in line:
                punc_idx = line.index('\n')
            else:
                punc_idx = len(line)
            line=line[:punc_idx]
            # label = int(line[0:1])
            # feature_line = line[2:punc_idx]
            words = line.split('\t')
            if cnt == 1:
                if len(words) == required_col_num and words[label_col_num]==label_col:
                    aaab=[]
                    for i,word in enumerate(words):
                        if word=='FPS_Id':word='id'
                        if word=='FPS': word='target'
                        if i in string_col_num:aaab.append(word)
                        if i != 0: write_file.write(',')
                        write_file.write(word)
                    write_file.write('\n')
                    print(aaab)
                    continue
                else:
                    break
            # cur_feature_list = []
            if len(words)!= required_col_num: continue
            for i,word in enumerate(words):
                if i !=0: write_file.write(',')
                if not word:
                    # cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    write_file.write('0')
                    continue
                if len(word) <= 0:
                    # cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    write_file.write('0')
                    continue
                if i==label_col_num:
                    # label=float(word)
                    write_file.write(str(float(word)))
                elif i in string_col_num:
                    m = hashlib.md5()
                    text = word

                    m.update(text.encode('utf-8'))
                    num = m.hexdigest()
                    num = int(num, 32) % (10 ** 8) / 2 ** 32
                    # num = (hash('Ultra'))
                    print(num)
                    # num=(hash(word) + 2.0 ** 31) / 2 ** 32
                    write_file.write(str(num))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(num)])
                elif i in date_col_num:
                ####handle date format
                    datetime_object = datetime.strptime(word, date_col_format.get(i))
                    feature_date = (datetime_object - ref_date).days
                    write_file.write(str(float(feature_date)))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(feature_date)])
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, word])
                ####handle date format
                else:
                    write_file.write(str(float(word)))
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, float(word)])
            # print(cur_feature_list)
            # features.append(cur_feature_list)
            # labels.append(label)
            write_file.write('\n')
            # if cnt == batch_size:
            #     yield labels, features
            #     labels = []
            #     features = []
            #     cnt = 0
    # if cnt > 0:
    #     yield labels, features
    write_file.close()
# load_data_from_file_batching('data/test.txt','data/FYPtestUpdate.csv')
# load_data_from_file_batching('data/train.txt','data/FYPtrainUpdate.csv')

load_data_from_file_batching('example/predict/predict.txt','example/predict/predict.csv')