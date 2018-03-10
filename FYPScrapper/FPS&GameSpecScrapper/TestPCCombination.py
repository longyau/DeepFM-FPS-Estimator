class CPU:
    # def __init__(self,name="",price="",score="",require=""):
    #     self.name=name
    #     self.price=price
    #     self.score=score
    #     self.require=require

    def printItem(self):
        return repr(self.__dict__)

class ComputeList:
    def __init__(self,CPU,MB,RAM):
        self.CPU=CPU
        self.MB=MB
        self.RAM=RAM
    def printItem(self):
        return repr('CPU:{0},MB:{1},RAM:{2}'.format(self.CPU.__dict__,self.MB.__dict__,self.RAM.__dict__))


# class MB:
#     def __init__(self,name="",price="",score="",require=""):
#         self.name=name
#         self.price=price
#         self.score=score
#         self.require=require
#     def printItem(self):
#         return repr(('Name:{0},Price:{1},Score:{2},Require:{3}'.format(self.name,self.price,self.score,self.require)))
#
# class RAM:
#     def __init__(self,name="",price="",score="",memory=0,qty=0,require=""):
#         self.name=name
#         self.price=price
#         self.score=score
#         self.memory=memory
#         self.qty=qty
#         self.require=require
#     def printItem(self):
#         return repr('Name:{0},Price:{1},Score:{2},Require:{3},SumMem{4}'.format(self.name,self.price,self.score,self.require,int(self.memory*self.qty)))
def readItem(file):
    itemList=[]
    with open(file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.endswith('\n'):
                line = line[:-1]
            if index == 0:
                cols = line.split("\t")
            else:
                properties = line.split("\t")
                obj = CPU()
                if len(cols) == len(properties):
                    for index, _ in enumerate(properties):
                        obj.__setattr__(cols[index], properties[index])
                itemList.append(obj)
    return itemList
_cpu,_ram,_mb=[],[],[]

_cpu=readItem('CPU.txt')
_ram=readItem('RAM.txt')
_mb=readItem('MB.txt')
# with open('CPU.txt') as f:
#     lines = f.readlines()
#     for index,line in enumerate(lines):
#         if line.endswith('\n'):
#             line=line[:-1]
#         if index==0:
#             cols=line.split("\t")
#             print(cols)
#         else:
#             properties=line.split("\t")
#             obj=CPU()
#             if len(cols)==len(properties):
#                 for index,_ in enumerate(properties):
#                     obj.__setattr__(cols[index],properties[index])
#             _cpu.append(obj)
#             # name, price, score, require = line.split("\t")
#             # _cpu.append(CPU(name,price,score,require))
# with open('MB.txt') as f:
#     lines = f.readlines()
#     for line in lines:
#         if line.endswith('\n'):
#             line = line[:-1]
#         name, price, score, require = line.split("\t")
#         _mb.append(MB(name, price, score, require))
# with open('RAM.txt') as f:
#     lines = f.readlines()
#     for line in lines:
#         if line.endswith('\n'):
#             line=line[:-1]
#         name,price,score,memory,qty,require=line.split("\t")
#         _ram.append(RAM(name,price,score,int(memory),int(qty),require))
Sum=0.0
computeList=[]
for cpu in _cpu:
    ratio=float(float(cpu.Score)/float(cpu.Price))
    Sum+=ratio
    cpu.__setattr__('price_score_ratio',ratio)
for cpu in _cpu:
    cpu.__setattr__('priority',float(cpu.price_score_ratio/Sum))
Sum = 0.0
for cpu in _mb:
    ratio=float(float(cpu.Score)/float(cpu.Price))
    Sum+=ratio
    cpu.__setattr__('price_score_ratio',ratio)
for cpu in _mb:
    cpu.__setattr__('priority',float(cpu.price_score_ratio/Sum))
Sum = 0.0
for cpu in _ram:
    ratio=float(float(cpu.Score)/float(cpu.Price))
    Sum+=ratio
    cpu.__setattr__('price_score_ratio',ratio)
for cpu in _ram:
    cpu.__setattr__('priority',float(cpu.price_score_ratio/Sum))
# for mb in _mb:
#     print(mb.printItem())
# for ram in _ram:
#     print(ram.printItem())

# for cpu in _cpu:
#     print(cpu.printItem())
# for mb in _mb:
#     print(mb.printItem())
# for ram in _ram:
#     print(ram.printItem())
for mb in _mb:
    for cpu in _cpu:
        if mb.Cpu_Socket==cpu.Cpu_Socket:
            if float(mb.Price)+float(cpu.Price)>3000:
                continue
            else:
            # print(cpu.priority*mb.priority)
            # obj = ComputeList(cpu,mb)
            # obj.__setattr__('ratio',cpu.priority*mb.priority)
            # computeList.append(obj)
                for ram in _ram:
                    if mb.Ram_Socket == ram.Ram_Socket:
                        obj = ComputeList(cpu,mb,ram)
                        obj.__setattr__('priority',cpu.priority*mb.priority*ram.priority)
                        computeList.append(obj)



for list in computeList:
    # for compon in list:
    #     print(compon.printItem())
    print(list.printItem())

    print('Priority',list.priority)