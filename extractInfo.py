import json
import datetime
import csv 
import sys
class cardData(object):
    def __init__(self,jsob,List,idtoName):
        """ Class containing msot relevant information from a trello card
        Attributes: 
            List (str): Specifies the list the card belongs to. 
            name (str): Card Title 
            due (datetime): date time object describing the due date for the card 
            desc (str):  string containing the cards discription. 
            url (str): string contiaing short url to this card 

        """
        self.List = List 
        self.name = jsob['name'] 
        self.due = jsob['due']
        self.completion = jsob['dueComplete']
        self.desc  = jsob['desc']
        self.url = jsob['shortUrl']
        self.labels= list()
        self.member = list()
        if jsob['idMembers']: #accounts for the lack of assigned people to cards 
            for p in jsob['idMembers']:
                self.member.append(idtoName[p]) 
        if jsob['due']: #accoounts for the lack of assigned due date 
            self.due= datetime.datetime.strptime(jsob['due'],'%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.due = datetime.datetime(2021,7,1)  
        if jsob['labels']:
            for l in jsob['labels']:
                self.labels.append(l['name'])
        print('The appended members or labels are: %s %s ' %(self.member,self.labels))

    def __str__(self):
        print(self.name)
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
        """" create list of strings to represent card in csv file """ 
        print(self.List) 
        return [self.name,self.List,self.due.date(),self.member,self.labels,self.desc,self.url]

def mergeList(a,b):
    merged = list() 
    for e in a: 
        merged.append(e)
    for e in b: 
        merged.append(e)
    if merged:
        return merged 
    else:
        merged.append('N/A')
        return merged 

def mapIDmembertoName(parsed_data):
    """ creates dictionary mapping user id to their actual name """
    idtoName = dict()
    for members in parsed_data['members']: 
        idtoName[members['id']]=members['fullName'] 
    return idtoName 

def mapListIdtoName(parsed_data):
    """ Creates dictionary mappin list id to it's name """ 
    idtoName= dict() 
    for e in parsed_data['lists']:
        idtoName[e['id']]=e['name']
    return idtoName

def consumeList(parsed_data,idtoName,memberMap):
    """ Take a list of trello cards in json format,create objects with the important info,
        cards are grouped by list """ 
    cardStack = dict()
    for e in parsed_data['cards']:
        if idtoName[e['idList']] in  cardStack:
            cardStack[idtoName[e['idList'] ]].append(cardData(e,idtoName[e['idList']],memberMap))
        else: 
            cardStack[idtoName[e['idList']]] = list()
            cardStack[idtoName[e['idList']]].append(cardData(e,idtoName[e['idList']],memberMap)) 
    return cardStack 
def flatCardStack(cardStack):
    """ takes card data and organizes it into a single list ordered by due date """
    data = list()
    for k in cardStack.keys():
        for e in cardStack[k]: 
            data.append(e) 
    return sorted(data) 


if __name__== '__main__':
    print('Attempting to open:  %s ' %sys.argv[1])
    data= open(sys.argv[1])
    parsed_data = json.load(data) 
    idToName = mapListIdtoName(parsed_data)
    memberMap = mapIDmembertoName(parsed_data) 
    things=  flatCardStack(consumeList(parsed_data,idToName,memberMap) )
    print(things)
    with open('output.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Card Name','List','Due Date','Asigned to','label','Description','url'])
        for e in things:
            writer.writerow(e.toCSV())
