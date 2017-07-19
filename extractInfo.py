import json
import datetime
import csv
import sys
import os
from cardData import cardData 
# class definition for object representing a  trello card
"""
    Script used to get jsonfile informaiton 
"""
def mapIDmembertoName(parsed_data):
    """ creates dictionary mapping user id to their actual name """
    idtoName = dict()
    for members in parsed_data['members']: 
        idtoName[members['id']]=members['fullName'] 
    return idtoName 

def mapListIdtoName(parsed_data):
    """ Creates dictionary mapping list id to it's name """ 
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
    return sorted(filter(lambda x: not( x.completion)  , data)) 
 
def main(s): 
    print('Attempting to open:  %s ' %s)
    #open and load data 
    data= open(s)
    parsed_data = json.load(data) 
    # create dictionaries  to map from trello id to board and from trello id to member 
    idToName = mapListIdtoName(parsed_data)
    memberMap = mapIDmembertoName(parsed_data) 
    # extract each idividual boards cards seperately then stack them together 
    things = flatCardStack(consumeList(parsed_data,idToName,memberMap))
    # writting each cards infomation one row at a time 
    with open('output.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Due Date ','Assigned To','Task','List','Description','Trello Assignment','url'])
        for e in things:
            writer.writerow(e.toCSV())
    print('Task is complete output.csv should be found in the path: %s ' %os.getcwd()  )
