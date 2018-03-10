class Component(object):
    ###temp use
    # def __init__(self):
        # self.Price=200.0
    ###temp use
    def add_info(self, name,value):
        self.__setattr__(name,value)
    def get_detail(self):
        return repr(self.__dict__)
class Computer_List:
    def __init__(self):
        self.compCount=0
    def add_component(self, name,object: Component):
        self.__setattr__(name,object)
        self.compCount+=1
    def get_all_components(self):
        components=[]
        names=[]
        for key,item in self.__dict__.items():
            if((type(item) is Component) and (len(components)<self.compCount)):
                components.append(item)
                names.append(key)
        return names,components


def readItem(file,_encoding='utf8'):
    itemList=[]
    Sum=0
    with open(file,encoding=_encoding) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            try:
                if line.endswith('\n'):
                    line = line[:-1]
                if line.endswith('\t'):
                    line = line[:-1]
                if index == 0:
                    cols = line.split("\t")
                else:
                    properties = line.split("\t")
                    obj = Component()
                    if len(cols) == len(properties):
                        for index2, _ in enumerate(properties):
                            if properties[index2] != '':
                                obj.add_info(cols[index2],properties[index2])
                            else:
                                print('Error Property{}'.format(cols[index2]))
                                raise AttributeError()
                        score=float(obj.Score)
                        price=float(obj.Price)
                        ratio=float(score/price)
                        # ratio = float(float(obj.Score) / float(obj.Price))
                        Sum += ratio
                        obj.add_info('price_score_ratio', ratio)
                        itemList.append(obj)
            except AttributeError:
                print('Index:{}Error'.format(index))
                continue
                # pass
    return itemList, Sum
_cpu,_ram,_mb=[],[],[]
_cpu,cpuSum=readItem('res/CPU_Data.txt')
_ram,ramSum=readItem('RAM.txt')
_mb,mbSum=readItem('MB.txt')
_computerList=[]
for cpu in _cpu:
    for ram in _ram:
        for mb in _mb:
            # if float(mb.Price)+float(cpu.Price)>3000:
            #     continue
            computerList=Computer_List()
            computerList.add_component('cpu',cpu)
            computerList.add_component('ram', ram)
            computerList.add_component('mb', mb)
            computerList.__setattr__('priority',(cpu.price_score_ratio/cpuSum*ram.price_score_ratio/ramSum*mb.price_score_ratio/mbSum))
            _computerList.append(computerList)
# for index,list in enumerate(_computerList):
#     keys,comps=list.get_all_components()
#     print('Index:{0},Priority{1}'.format(index,list.priority))
#     for comp in comps:
#         print(comp.get_detail())
_computerList.sort(key=lambda p:p.priority)
for index,list in enumerate(_computerList):
    keys,comps=list.get_all_components()
    print('Index:{0},Priority{1}'.format(index,list.priority))
    for comp in comps:
        print(comp.get_detail())