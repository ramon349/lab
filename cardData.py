import datetime
class cardData(object):
    def __init__(self, jsob, List, idtoName):
        """ Class containing most relevant information from a trello card
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
        self.completion = jsob['closed']
        self.desc = jsob['desc']
        self.url = jsob['shortUrl']
        self.labels = ", "
        self.member = ", " 

        if jsob['idMembers']:  #accounts for the lack of assigned people to cards :
            self.member = self.member.join(list(map(lambda x: idtoName[x],jsob['idMembers'])))
        else: 
            self.member = "N/A"
        if jsob['due']: 
            self.due= datetime.datetime.strptime(jsob['due'],'%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.due = datetime.datetime(2021,7,1)# if due date exist i set july 1,2021 as the "due" date 
        if jsob['labels']:
            self.labels = self.labels.join( list(filter(lambda x: x , list(map(lambda x:  x['name'],jsob['labels'])) ) ) ) 
        else: 
            self.labels = "N/A"
    def toCSV(self):
        """" create list of strings to represent card in csv file """ 
        return [self.due.date(),self.labels,self.name,self.List,self.desc,self.member,self.url]
   #string representation of the object  
    def __str__(self):
        return self.name
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
