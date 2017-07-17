import json
import datetime
import csv 
import sys
import os 
class cardData(object):
    def __init__(self,jsob,List,idtoName):
        """ Class containing msot relevant information from a trello card
        Attributes: 
            List (str): Specifies the list the card belongs to. 
            name (str): Card Title 
            due (datetime): date time object describing the due date for the card 
            desc (str):  string containing the cards discription. 
            url (str): string contiaing short url to this card 
            member(str):  string representing all the people assigned to that card 
            labels (str): string containing trello cards label information 
            completion (bool): boolean representing whether the task was completed 

        """
        self.List = List 
        self.name = jsob['name'] 
        self.due = jsob['due']
        self.completion = jsob['dueComplete']
        self.desc  = jsob['desc']
        self.url = jsob['shortUrl']
        self.labels= ""
        self.member = "" 

        if jsob['idMembers']: #accounts for the lack of assigned people to cards 
            for p in jsob['idMembers']:
                self.member=self.member + ", "  +  idtoName[p]
        else: 
            self.member = "N/A"

        if jsob['due']: 
            self.due= datetime.datetime.strptime(jsob['due'],'%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.due = datetime.datetime(2021,7,1)# if due date exist i set july 1,2021 as the "due" date 

        if jsob['labels']:
            for l in jsob['labels']:
                self.labels = self.labels + ", " +  l['name']
        else: 
            self.labels = "N/A" 

    #string representation of the object 
    def __str__(self):
        return   self.name
    def __repr__(self): 
        return  self.name 

    #functions used whenver the object is to be compared i.e( x<y and such  ) 
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
        return [self.due.date(),self.labels,self.name,self.List,self.desc,self.member,self.url]

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
    #open and load data 
    data= open(sys.argv[1])
    parsed_data = json.load(data) 
    # create ditionaries to map from trello id to board and from trello id to member 
    idToName = mapListIdtoName(parsed_data)
    memberMap = mapIDmembertoName(parsed_data) 
    # extract each idividual boards cards seperately then stack them together 
    things=  flatCardStack(consumeList(parsed_data,idToName,memberMap) ) 
    # writting each cards infomation one row at a time 
    with open('output.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Due Date ','Assigned To','Task','List','Description','Trello Assignment','url'])
        for e in things:
            writer.writerow(e.toCSV())
    print('Task is complete output.csv should be found in the path: %s ' %os.getcwd()  )
