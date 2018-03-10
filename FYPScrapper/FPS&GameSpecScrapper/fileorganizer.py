import csv
with open('res/CPU_Data.csv','r', encoding = 'utf8') as orgData:
    with open('res/newData.txt','w',encoding='utf8') as newData:
        reader=csv.reader(orgData, delimiter=',')
        fieldnames = ['Type','Part','Brand','Model','Rank','Score','Samples','URL','Name','Codename','Cores','Socket','Process','Clock','Multi','Cache L1/L2/L3','TDP','Released']
        for field in fieldnames:
            newData.write(field+'\t')
        newData.write('\n')
        for index,row in enumerate(reader):
            if(index%2==0):
                print(row)
                for itm in row:
                    newData.write(itm + '\t')
                newData.write('\n')