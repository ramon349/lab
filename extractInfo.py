import json
import datetime
import csv 
class cardData(object):
    def __init__(self,jsob,List):
        self.List = List 
        self.name = jsob['name'] 
        self.due = jsob['due']
        self.completion = jsob['dueComplete']
        self.desc  = jsob['desc']
        if jsob['due']:
            self.due= datetime.datetime.strptime(jsob['due'],'%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.due = None 

    def __str__(self):
        print(self.due)
        return   self.name
    def __repr__(self): 
        return  self.name 
    def __lt__(self,other):
        return self.due < other.due 
    def __le__(self,other):
        return self.due<= other.due 
    def __eq__(self,other): 
        return self.due == other.due 
    def __ne__(self,other):
        return self.due != other.due 
    def __gt__(self,other):
        return self.due > other.due 
    def __ge__(self,other):
        return self.due >= otehr.due 
    def toCSV(self):
        return [self.name,self.due.date(),self.desc]

def mapListIdtoName(parsed_data):
    idtoName= dict() 
    for e in parsed_data['lists']:
        idtoName[e['id']]=e['name']
    return idtoName
def consumeList(parsed_data,idtoName):
    cardStack = dict()
    for e in parsed_data['cards']:
        if idtoName[e['idList']] in  cardStack:
            cardStack[idtoName[e['idList'] ]].append(cardData(e,e['idList']))
        else: 
            cardStack[idtoName[e['idList']]] = list()
            cardStack[idtoName[e['idList']]].append(cardData(e,e['idList'])) 
    return cardStack 
if __name__== '__main__':
    print('hello World')
    data= open('trello2.json')
    parsed_data = json.load(data) 
    idToName = mapListIdtoName(parsed_data)
    things=  consumeList(parsed_data,idToName) 
    with open('output.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Card Name','Due Date','Description'])
        for k in things.keys():
            for e in sorted(things[k]):
                writer.writerow(e.toCSV())
