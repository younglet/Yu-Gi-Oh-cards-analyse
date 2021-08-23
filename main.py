import random
import itertools


class Card():
    #定义卡片类，卡片包含卡名、种类和ID，其中ID用于区分同名卡
    def __init__(self, name, kind, id) -> None:
        self.id = id
        self.name = name
        self.kind = kind

    # 展示卡片的信息
    def showInfo(self):
        print('id:\t{}，\tcard:\t{},\t\tkind:\t{}'.format(self.id, self.name, self.kind))

class Set():
    #定义卡组类，卡组包含包含所有卡片的列表，并会生产包含所有可能情况的先、后攻的手牌
    def __init__(self, file_name) -> None:
        self.countForCardId = 0
        self.cards = []
        self.firstHands = []
        self.secondHands = []
        self.load_file(file_name)
        self.addCard(self.data_lines)
    
    #读取txt文本中的卡组信息
    def load_file(self,file_name):
        with  open(file_name,'r') as f:
            self.data_lines = f.readlines()
        print('读取卡组文件成功.......')

    #根据载入的卡组信息，往卡片中添加卡片信息
    def addCard(self,data_lines):
        for data_line in data_lines:
            data_line = data_line.strip('\n').split()
            for _ in range(int(data_line[2])):
                self.countForCardId += 1
                card_name = data_line[0]
                card_kind = data_line[1]
                card_id = self.countForCardId
                self.cards.append(Card(card_name, card_kind, card_id))
        print('卡组载入成功，以下为卡片列表：')
        self.showCardsList()
    
    #打印卡组的数量
    def showCardsAmount(self):
        print('the amount of cards is {}'.format(len(self.cards)))

    #展示卡组每张卡牌的信息
    def showCardsList(self):
        for card in self.cards:
            card.showInfo()

class Hand():

    #定义手牌，先攻后攻都是使用这个类，根据手牌的情况生成卡片信息列表
    def __init__(self,cards) -> None:
        self.cards = cards
        self.generateResDict()

    #展示手牌每张卡牌的信息
    def showInfo(self):
        for card in self.cards:
            card.showInfo()

    #根据手帕卡片的种类生成用于比较的字典{卡名：数量}
    def generateResDict(self):
        self.resDict = {}
        for card in self.cards:
            self.resDict[card.name] = self.resDict.get(card.name,0) +1
    #展示用于比较的信息字典
    def showResDict(self):
        print(self.resDict)

    #检查是否符合传入的卡片组合，如果符合则返回True，否则为False；数量严格相等，数量多的情况不包含数量少的情况。
    def checkCombaination(self, combination):
        for key in combination:
            if key not in self.resDict.keys():
                return False
            if self.resDict[key] != int(combination[key]):
                return False
        return True
                
class Parser():

    #传入卡组，生成所有可能性的先后手起手；并读取文件或许要分析的卡片组合
    def __init__(self,set, file_name) -> None:
        self.set = set
        self.generatePossibleFirstHands()
        self.generatePossibleSecondHands()
        self.load_file(file_name)
        self.getCombinations()

    #生成所有可能的先攻手牌
    def generatePossibleFirstHands(self):
        self.firstHands = []
        for cards in itertools.combinations(self.set.cards,4):
            self.firstHands.append(Hand(cards))
        self.firstHandsAmount = len(self.firstHands)
        print('先攻一共有：{}种情况'.format(self.firstHandsAmount))

    #生成所有可能的后攻手牌
    def generatePossibleSecondHands(self):
        self.secondHands = []
        for cards in itertools.combinations(self.set.cards,5):
            self.secondHands.append(Hand(cards))
        self.secondHandsAmount = len(self.secondHands)
        print('后攻一共有：{}种情况'.format(self.secondHandsAmount))

    #载入待查询卡片组合的txt文本
    def load_file(self,file_name):
        with  open(file_name,'r') as f:
            self.data_lines = f.readlines()
        print('读取待查询文件文件成功.......')

    #根读取的组合txt文件，将每个组合作为元素转化为列表
    def getCombinations(self):
        self.combinations = []
        for data_line in self.data_lines:
            data_line.strip('\n')
            self.combinations.append(data_line.split())

    #解析所有可能的组合
    def parserCombination(self):
        with open('result.txt','w') as f:
            #变量所有待查询的组合，转换为用于比较的字典
            for combination in self.combinations:
                combination = dict(zip(combination[::2],combination[1::2]))

                #遍历所有的先攻手牌，检查是否符合正在查询的卡片组合，并做相应的记录，最后打印并写入文件。
                count = 0
                for hand in self.firstHands:
                    if hand.checkCombaination(combination):
                        count += 1
                f.write('先攻情况下， {}组合一共出现{}次,出现的概率是{:.3%}\n'.format(combination, count, count/self.firstHandsAmount))
                print('先攻情况下， {}组合一共出现{}次,出现的概率是{:.3%}'.format(combination, count, count/self.firstHandsAmount))
                
                #遍历所有的后攻手牌，检查是否符合正在查询的卡片组合，并做相应的记录，最后打印并写入文件。
                count = 0
                for hand in self.secondHands:
                    if hand.checkCombaination(combination):
                        count += 1
                f.write(('后攻情况下， {}组合一共出现{}次,出现的概率是{:.3%}\n'.format(combination, count, count/self.secondHandsAmount)))
                print('后攻情况下， {}组合一共出现{}次,出现的概率是{:.3%}'.format(combination, count, count/self.secondHandsAmount))


my_set = Set('set.txt')                             #实例卡组，载入卡组文件
my_parser = Parser(my_set, 'combination.txt')       #实例生成器，载入待查询组合文件
my_parser.parserCombination()                       #对卡组进行解析